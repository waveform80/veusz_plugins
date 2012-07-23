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

"""Utilities for veusz plugins"""

import sys
import re

def sanitize_name(name):
    "Removes characters from name until its empty or a valid Python identifier"
    # Python 3 permits Unicode letters in identifiers
    if sys.hexversion >= 0x03000000:
        first_letter = re.compile(r'[^\d\W]', re.UNICODE)
        other_letters = re.compile(r'\w', re.UNICODE)
    else:
        first_letter = re.compile(r'[^\d\W]')
        other_letters = re.compile(r'\w')
    for index, char in enumerate(name):
        if first_letter.match(char):
            return char + ''.join(c for c in name[index + 1:] if other_letters.match(c))

def sanitize_names(names):
    "Sanitizes all names as Python identifiers, and ensures no duplicates"
    names = [sanitize_name(name) for name in names]
    counts = dict((name, names.count(name)) for name in names)
    result = []
    for name in reversed(names):
        if counts[name] == 1:
            result.append(name)
        else:
            result.append(name + unicode(counts[name]))
            counts[name] -= 1
    result.reverse()
    return result

