# vim: set et sw=4 sts=4:

# Copyright 2012 Dave Hughes.
#
# This file is part of veusz-plugins.
#
# veusz-plugins is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# veusz-plugins is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# veusz-plugins.  If not, see <http://www.gnu.org/licenses/>.

"""Plugin supporting import of Excel worksheets into Veusz"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

from veusz.plugins import (
    ImportPlugin,
    ImportDataset1D,
    ImportDatasetText,
    FieldCombo,
    FieldText,
    FieldBool,
    importpluginregistry,
    )

import re
import xlrd
from veusz_plugins.utils import sanitize_names

def used_range(sheet):
    "Calculate the range of used cells on the specified worksheet"
    blank = (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK, xlrd.XL_CELL_ERROR)
    first_row = first_col = last_row = last_col = None
    for row in range(sheet.nrows):
        if any(cell.ctype not in blank for cell in sheet.row(row)):
            first_row = row
            break
    for col in range(sheet.ncols):
        if any(cell.ctype not in blank for cell in sheet.col(col)):
            first_col = col
            break
    for row in reversed(range(sheet.nrows)):
        if any(cell.ctype not in blank for cell in sheet.row(row)):
            last_row = row
            break
    for col in reversed(range(sheet.ncols)):
        if any(cell.ctype not in blank for cell in sheet.col(col)):
            last_col = col
            break
    return '{top_left}:{bottom_right}'.format(
        top_left=xlrd.cellname(first_row, first_col),
        bottom_right=xlrd.cellname(last_row, last_col))

def parse_col(col):
    "Convert a column specification to a zero-based offset"
    col = col.upper()
    result = 0
    while col:
        result *= 26
        result += ord(col[0]) - ord('A') + 1
        col = col[1:]
    result -= 1
    if 0 <= result <= 255:
        return result
    else:
        raise xlrd.XLRDError('Column must be between A and IV')

def parse_cell(name):
    "Convert a textual cell reference to a zero-based (row, col) tuple"
    match = re.match(r'^([a-zA-Z]+)(\d+)$', name)
    if not match:
        raise xlrd.XLRDError('Invalid cell reference: {}'.format(name))
    col, row = match.groups()
    return int(row) - 1, parse_col(col)

def parse_range(ref):
    "Convert a textual range reference to two cell tuples"
    if not ':' in ref:
        raise xlrd.XLRDError('Expected : separator in range')
    cell1, cell2 = ref.split(':', 1)
    cell1, cell2 = parse_cell(cell1), parse_cell(cell2)
    # Sort out weird backwards ranges
    first_row, last_row = sorted((cell1[0], cell2[0]))
    first_col, last_col = sorted((cell1[1], cell2[1]))
    return ((first_row, first_col), (last_row, last_col))


class ImportPluginExcel(ImportPlugin):
    """A plugin supporting Excel workbooks"""

    name = 'Excel import'
    author = 'Dave Hughes <dave@waveform.org.uk>'
    description = 'Reads data from Excel workbooks'
    file_extensions = set(['.XLS', '.xls'])

    def __init__(self):
        ImportPlugin.__init__(self)
        self.fields = [
            FieldCombo('direction', descr='Direction', items=['Columns', 'Rows'], editable=False),
            FieldText('sheet', descr='Sheet (defaults to first)'),
            FieldText('range', descr='Range (defaults to used range)'),
            FieldBool('header', descr='Treat first row/col as dataset names'),
        ]

    def getPreview(self, params):
        try:
            workbook = xlrd.open_workbook(params.filename)
            result = 'File contains {nsheets} sheets: {names}\n'.format(
                nsheets=workbook.nsheets,
                names=','.join(workbook.sheet_names()))
            for sheet in workbook.sheets():
                result += 'Sheet "{name}" has used range {range}\n'.format(
                    name=sheet.name,
                    range=used_range(sheet))
            sheet = params.field_results.get('sheet')
            if sheet:
                # Test whether the specified sheet exists
                workbook.sheet_by_name(sheet)
            ref = params.field_results.get('range')
            if ref:
                # Test whether the specified range is parseable
                parse_range(ref)
            return (result, True)
        except IOError as exc:
            return ('I/O error when reading file: {}'.format(exc), False)
        except xlrd.XLRDError as exc:
            return (unicode(exc), False)

    def doImport(self, params):
        workbook = xlrd.open_workbook(params.filename)
        sheet = params.field_results.get('sheet', '')
        if not sheet:
            sheet = '0'
        if sheet.isdigit():
            # If the name is entirely numeric, treat it as a zero-based sheet
            # index instead of a name
            sheet = workbook.sheet_by_index(int(sheet))
        else:
            sheet = workbook.sheet_by_name(sheet)
        ref = params.field_results.get('range', '')
        if not ref:
            ref = used_range(sheet)
        (first_row, first_col), (last_row, last_col) = parse_range(ref)
        # Clamp the selected range to the used cells on the sheet
        last_row = max(sheet.nrows - 1, last_row)
        last_col = max(sheet.ncols - 1, last_col)
        if params.field_results.get('direction', 'Columns') == 'Columns':
            if params.field_results.get('header', False):
                names = [
                    unicode(cell.value)
                    for cell in sheet.row(first_row)[first_col:last_col + 1]]
                first_row += 1
            else:
                names = [
                    'col{}'.format(xlrd.colname(i))
                    for i in range(first_col, last_col + 1)]
            data = [
                [cell for cell in sheet.col(col)[first_row:last_row + 1]]
                for col in range(first_col, last_col + 1)]
        else:
            if params.field_results.get('header', False):
                names = [
                    unicode(cell.value)
                    for cell in sheet.col(first_col)[first_row:last_row + 1]]
                first_col += 1
            else:
                names = [
                    'row{}'.format(i)
                    for i in range(first_row, last_row + 1)]
            data = [
                [cell for cell in sheet.row(row)[first_col:last_col + 1]]
                for row in range(first_row, last_row + 1)]
        names = sanitize_names(names)
        classes = [
            ImportDatasetText if any(cell.ctype == xlrd.XL_CELL_TEXT for cell in col) else ImportDataset1D
            for col in data]
        result = []
        for (name, cls, column) in zip(names, classes, data):
            if cls is ImportDataset1D:
                result.append(ImportDataset1D(
                    name, data=[
                        # Import non-numeric cells as NaN
                        float(cell.value) if cell.ctype == xlrd.XL_CELL_NUMBER else float('NaN')
                        for cell in column]))
            else:
                result.append(ImportDatasetText(
                    name, data=[
                        cell.value if cell.ctype == xlrd.XL_CELL_TEXT else ''
                        for cell in column]))
        return result

importpluginregistry.append(ImportPluginExcel)


