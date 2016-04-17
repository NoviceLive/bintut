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

sys.path.append(resource_filename(__name__, ''))

from courses.main import start_tutor


if __name__ == '__main__':
    # This does not seem to work inside GDB Python.
    from os.path import join, isdir
    from atexit import register
    try:
        import readline
    except ImportError:
        pass
    history_dir = '.'
    history = join(history_dir, 'history')
    try:
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode emacs')
    except NameError:
        pass
    try:
        readline.read_history_file(history)
    except (NameError, OSError):
        pass
    if isdir(history_dir):
        try:
            register(readline.write_history_file, history)
        except NameError:
            pass

    start_tutor(course, bits, burst, aslr, level)
