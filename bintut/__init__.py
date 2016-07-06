"""
Copyright 2016 Gu Zhengxiong <rectigu@gmail.com>

This file is part of BinTut.

BinTut is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BinTut is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BinTut.  If not, see <http://www.gnu.org/licenses/>.
"""


from __future__ import division, absolute_import, print_function
import sys

from pkg_resources import resource_filename


__author__ = 'Gu Zhengxiong'

version_file = resource_filename(__name__, 'version.txt')
with open(version_file) as stream:
    __version__ = stream.read().strip()

PROGRAM_NAME = 'BinTut'
PACKAGE_NAME = PROGRAM_NAME.lower()

VERSION_PROMPT = (
    '{}\n\nCopyright 2016 {} <rectigu@gmail.com>\n\n'
    'This is free software; see the source for '
    'copying conditions.\nThere is NO warranty; '
    'not even for MERCHANTABILITY nor \nFITNESS FOR '
    'A PARTICULAR PURPOSE.\n\nPython, version {}'.format(
        __version__, __author__, sys.version)
)
