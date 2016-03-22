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


try:
    import gdb
except ImportError:
    pass


# TODO: Make it a class.
def Addr(func_name):
    if func_name == '/bin/sh':
        return get_bin_sh_str()
    elif func_name == 'leave_ret':
        return get_leave_ret_gadget()
    else:
        raw = gdb.execute('p {}'.format(func_name), to_string=True)
        addr = raw.split()[-2]
        return addr


def get_leave_ret_gadget():
    # TODO: Remove hardcoded behaviors.
    leave = gdb.execute('disas read_file',
                        to_string=True).splitlines()[-3]
    return leave.split()[0]


def get_bin_sh_str():
    start = Addr('__libc_start_main')
    print('!!! executing find...')
    found = gdb.execute('find {}, +2000000, "/bin/sh"'.format(
        start), to_string=True)
    print(found)
    binsh = found.splitlines()[0]
    return binsh


def get_bits():
    name = gdb.selected_frame().architecture().name()
    return 32 if name == 'i386' else 64


def get_size_of_pointer():
    return 4 if get_bits() == 32 else 8
