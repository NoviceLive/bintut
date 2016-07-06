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
from binascii import hexlify

from pkg_resources import resource_filename
from pat import Pat

from .init import LevelFormatter, cyan
from .utils import select_target
from .repl import redisplay
from .exploits import Environment, make_payload
from .utils import pause, get_libc_path


pat = Pat()
debugger = None


def start_tutor(course, bits, burst, aslr, level):
    Environment(bits=bits, aslr=aslr)
    global debugger
    debugger = Environment.debugger

    logger = logging.getLogger()
    handler = logging.StreamHandler(stderr)
    handler.setFormatter(LevelFormatter())
    logger.addHandler(handler)
    logger.setLevel(level)

    try:
        bin_name = select_target(course, Environment.PLATFORM, bits)
    except ValueError as error:
        logging.error(error)
        exit(1)
    root = resource_filename(__name__, '')
    target = realpath(join(root, 'targets', bin_name))
    Environment.LIBC_PATH = get_libc_path(target)
    logging.debug('target: %s', target)
    logging.debug('libc: %s', Environment.LIBC_PATH)

    name = '{}-{}.bin'.format(course, 'x86' if bits == 32 else 'x64')
    name = realpath(name)
    with open(name, 'w') as stream:
        stream.write(pat.create(400))

    offset, addr = pattern_locatable(target, name, bits,
                                     burst, course)
    if offset:
        logging.info('\nFound offset: %s', offset)
        payload = make_payload(offset, addr, course)
        logging.info('Writing payload: %s', name)
        count = payload.count(b'\00')
        if count:
            logging.warning('Payload contains %s NULL bytes!', count)
        with open(name, 'wb') as stream:
            stream.write(payload)
        # TODO: Implement a pretty printer for humans.
        logging.info('%s Bytes', len(payload))
        logging.info('Payload: %s', payload)
        logging.info('Hexlified: %s', hexlify(payload))
        pause(cyan('Enter to test the payload...'))
        pattern_locatable(target, name, bits, burst, course)
    else:
        logging.error('Offset Not Found')


def pattern_locatable(target, name, bits, burst, course):
    debugger.start(target, [name])
    last_stack = ''
    while True:
        try:
            cur_stack = debugger.get_stack()
            last_stack = cur_stack
        except IOError as error:
            if bits == 64:
                debugger.start(target, [name])
                logging.error(last_stack)
                pattern = last_stack.split()[1]
                try:
                    offset = pat.locate(pattern)
                except (KeyError, UnicodeDecodeError) as error:
                    logging.error(error)
                    logging.error('Exiting Gracefully...')
                    break
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
            ip = debugger.get_pc_asm()
        except IOError as error:
            addr, pattern = error.args
            try:
                offset = pat.locate(pattern)
            except UnicodeDecodeError as error:
                logging.error(error)
                logging.error('Exiting Gracefully...')
                break
            logging.info('addr: %s offset: %s', addr, offset)
            if burst:
                pass
            else:
                pause('Enter to return...')
            return offset, addr
        # TODO: Remove hardcoded behaviors.
        def inside_fun(ip, fun):
            return ('<{}>'.format(fun) in ip or
                    '(_{})'.format(fun) in ip)
        def is_read_file(ip):
            return inside_fun(ip, 'read_file')
        def is_off_by_one(ip):
            return inside_fun(ip, 'off_by_one')
        if 'call' in ip and (is_read_file(ip) or is_off_by_one(ip)):
            debugger.step()
        elif '<system>' in ip and burst:
            debugger.cont()
        elif 'call' in ip:
            debugger.next()
        else:
            try:
                debugger.step()
            except KeyboardInterrupt:
                break
            except IOError:
                pass
        redisplay(debugger, burst=burst, target=relpath(target),
                  course=course)
    return None, None
