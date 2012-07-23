#!/usr/bin/env python
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

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

from setuptools import setup, find_packages
from utils import description, get_version, require_python

# Workaround <http://bugs.python.org/issue10945>
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

require_python(0x020600f0)

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Win32 (MS Windows)',
    'Environment :: X11 Applications :: Qt',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Multimedia :: Graphics',
    'Topic :: Scientific/Engineering',
]


def main():
    setup(
        name                 = 'veusz_plugins',
        version              = get_version('veusz_plugins/__init__.py'),
        description          = 'A collection of miscellaneous plugins for the veusz graphing application',
        long_description     = description('README.txt'),
        author               = 'Dave Hughes',
        author_email         = 'dave@waveform.org.uk',
        url                  = 'https://github.com/waveform80/veusz_plugins',
        packages             = find_packages(exclude=['distribute_setup', 'utils']),
        install_requires     = ['xlrd']
        platforms            = 'ALL',
        zip_safe             = False,
        classifiers          = classifiers
    )

if __name__ == '__main__':
    main()
