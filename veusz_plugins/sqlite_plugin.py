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

"""Plugin supporting import of SQLite query results into Veusz"""

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
    FieldText,
    importpluginregistry,
    )

import sqlite3
from veusz_plugins.utils import sanitize_names

class ImportPluginSQLite(ImportPlugin):
    """A plugin supporting SQLite databases"""

    name = 'SQLite import'
    author = 'Dave Hughes <dave@waveform.org.uk>'
    description = 'Reads data from queries against an SQLite database'

    def __init__(self):
        ImportPlugin.__init__(self)
        self.fields = [
            FieldText('query', descr='SQL query'),
        ]

    def getPreview(self, params):
        try:
            conn = sqlite3.connect(params.filename)
            cursor = conn.cursor()
            # List the tables in the database
            try:
                cursor.execute("""\
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table'
                    ORDER BY name""")
                result = 'Database contains the following tables:\n'
                result += '\n'.join(row[0] for row in cursor)
            finally:
                conn.rollback()
            # Test the user's query (if any)
            query = params.field_results.get('query')
            if query:
                try:
                    cursor.execute(query)
                finally:
                    conn.rollback()
            return (result, True)
        except sqlite3.Error as exc:
            return (unicode(exc), False)

    def doImport(self, params):
        conn = sqlite3.connect(params.filename)
        cursor = conn.cursor()
        query = params.field_results.get('query')
        cursor.execute(query)
        # We can only iterate through the cursor once (standard forward-only
        # semantics) so here we convert the query result to a list for further
        # processing
        data = [row for row in cursor]
        # Transpose the data from a list of row-tuples to a list of columns
        data = [
            [row[i] for row in data]
            for i, col in enumerate(cursor.description)]
        # Figure out the dataset name and type for each column
        names = sanitize_names(col[0] for col in cursor.description)
        classes = [
            ImportDatasetText if any(isinstance(value, basestring) for value in column) else ImportDataset1D
            for column in data]
        result = []
        for (name, cls, column) in zip(names, classes, data):
            if cls is ImportDataset1D:
                result.append(ImportDataset1D(
                    name, data=[
                        # Import NULL values as NaN in numeric datasets
                        float('NaN') if value is None else float(value)
                        for value in column]))
            else:
                result.append(ImportDatasetText(
                    name, data=[
                        # Import NULL values as blank strings in text datasets
                        '' if value is None else value
                        for value in column]))
        return result

importpluginregistry.append(ImportPluginSQLite)



