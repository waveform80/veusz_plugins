.. -*- rst -*-

=============
veusz-plugins
=============

This package contains a collection of plugins written for the Veusz scientific
graphing application. The plugins are mostly concerned with data-import,
providing support for the following formats / sources:

 * Microsoft Excel workbooks
 * SQLite databases


Pre-requisites
==============

veusz-plugins obviously depends on the veusz application itself. Additional
dependencies are:

 * `xlrd <http://pypi.python.org/pypi/xlrd>`_ - required for Excel import


Installation
============

After installing the package, start Veusz and select Preferences from the Edit
menu. Select the Plugins tab at the far right of the dialog that appears. Click
on the Add... button and navigate to the directory that the plugins were
installed into. On Linux this will be something one of the following:

 * /usr/lib/python2.7/dist-packages/veusz_plugins/
 * /usr/local/lib/python2.7/dist-packages/veusz_plugins/

Select the xls_plugin.py module in this directory and click on Open. Once back
at the preferences dialog, do the same for sqlite_plugin.py. Finally, click on
OK then exit and restart Veusz. The plugins will only be available after such a
restart.


Excel import
============

The Excel import plugin can be found under the "Plugins" tab of the data import
dialog. Select an Excel file, then optionally enter the sheet name and range
that you wish to import. If the sheet name is left blank, the first sheet in
the file will be used. If the range is left blank then all used cells within
the selected sheet will be imported. Sheet names are considered case sensitive
and ranges are specified as standard 2D ranges are expressed in Excel (e.g.
"A1:D28").

You can select whether to to treat columns or rows as sets of data (default is
columns) and whether or not to treat the first row or column of data as the
names of the datasets. If the latter option is not selected then datasets will
be named after the column or row that they were imported from.

If the source range for a dataset contains one or more cells containing text,
the dataset created from the range will be a text dataset which can only be
used as labels. Numeric datasets will only be created if the entire range is
numeric/blank.

Blank cells within text ranges are imported as blank strings. Blank cells
within numeric ranges are imported as NaN (not-a-number) values.


SQLite import
=============

The SQLite import plugin can be found under the "Plugins" tab of the data
import dialog.  Select an SQLite database file, then enter the query that you
wish to execute against it and click Import. To aid you in writing the query,
the set of tables available in the databaes will be listed in the data preview.

Each column of the query's result set will be converted into a dataset. Column
names that are not valid Python identifiers will be automatically converted
into valid identifiers.

If a column contains entirely numeric data or NULLs it will be treated as a
numeric dataset, otherwise it will be treated as a text dataset which can only
be used as labels.  NULL values within text datasets are imported as blank
strings. NULL values within numeric datasets are imported as NaN (not-a-number)
values.


License
=======

This file is part of veusz-plugins.

veusz-plugins is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

veusz-plugins is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
veusz-plugins.  If not, see <http://www.gnu.org/licenses/>.
