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
from logging import getLogger

try:
    import gdb
except ImportError:
    pass

from .init import red, yellow


logging = getLogger(__name__)


def align_to_page(addr):
    return hex(int(addr, 16) & ~4095)


def align_32(addr):
    return '{:#010x}'.format(int(addr, 16)) if addr else ''


def align_64(addr):
    return '{:#018x}'.format(int(addr, 16)) if addr else ''


# TODO: Make it a class.
# TODO: Use other libraries.
def Addr(func_name, bits=32):
    if func_name == '/bin/sh':
        addr = get_bin_sh_str(bits)
    else:
        raw = gdb.execute('p {}'.format(func_name), to_string=True)
        addr = raw.split()[-2]
    addr = addr if bits == 32 else align_64(addr)
    print(yellow(func_name), red(addr))
    return addr


def get_bin_sh_str(bits):
    # TODO: Remove hardcoded ad-hoc behaviors.
    # TODO: Use other libraries.
    start = Addr('__libc_start_main', bits)
    command = 'find {}, +2000000, "/bin/sh"'.format(start)
    found = gdb.execute(command, to_string=True)
    bin_sh = found.splitlines()[0]
    return bin_sh
