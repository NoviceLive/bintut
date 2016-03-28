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


def align_addr_64(addr):
    return '{:#018x}'.format(int(addr, 16))


# TODO: Make it a class.
# TODO: Use other libraries.
def Addr(func_name, bits=32):
    if func_name == '/bin/sh':
        addr = get_bin_sh_str(bits)
    elif func_name == 'leave_ret':
        addr = get_leave_ret_gadget()
    else:
        raw = gdb.execute('p {}'.format(func_name), to_string=True)
        addr = raw.split()[-2]
    addr = addr if bits == 32 else align_addr_64(addr)
    print(yellow(func_name), red(addr))
    return addr


def get_leave_ret_gadget():
    # TODO: Remove hardcoded ad-hoc behaviors.
    # TODO: Use other libraries.
    leave = gdb.execute('disas read_file',
                        to_string=True).splitlines()[-3]
    gadget = leave.split()[0]
    return gadget


def get_bin_sh_str(bits):
    # TODO: Remove hardcoded ad-hoc behaviors.
    # TODO: Use other libraries.
    start = Addr('__libc_start_main', bits)
    command = 'find {}, +2000000, "/bin/sh"'.format(start)
    found = gdb.execute(command, to_string=True)
    bin_sh = found.splitlines()[0]
    return bin_sh


def get_bits():
    name = gdb.selected_frame().architecture().name()
    return 32 if name == 'i386' else 64


def get_size_of_pointer():
    return 4 if get_bits() == 32 else 8
