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
from binascii import unhexlify
from sys import platform as sys_platform
from collections import defaultdict
from subprocess import check_output
from os.path import realpath


logging = getLogger(__name__)


def get_libc_path(elf):
    output = check_output(['ldd', elf], universal_newlines=True)
    for line in output.splitlines():
        if 'libc.so.6' in line:
            path = line.split()[2]
            break
    else:
        raise RuntimeError('Failed to find the path to libc.')
    return realpath(path)

# TODO: Use other libraries.
def simple_platform():
    """Simple."""
    if sys_platform in ['linux', 'linux2']:
        return 'linux'
    elif sys_platform in ['win32']:
        return 'win32'
    else:
        raise ValueError('Unknow platform: {}'.format(sys_platform))


def tree():
    return defaultdict(tree)


# TODO: Find a better way and group with ``bintut -l``.
def select_target(course, platform, bits):
    logging.debug('course: %s', course)
    logging.debug('platform: %s', platform)
    logging.debug('bits: %s', bits)
    if bits == 64 and course in ['ret2lib', 'frame-faking']:
        raise ValueError('Course only available in x86!')
    courses = tree()
    courses['linux']['plain'] = 'fread-nx_off-canary_off-{}'
    courses['linux']['nop-slide'] = 'fread-nx_off-canary_off-{}'
    courses['linux']['jmp-esp'] = 'fread-nx_off-canary_off-{}'
    courses['linux']['ret2lib'] = 'fread-nx_on-canary_off-x86'
    courses['linux']['frame-faking'] = 'fread-nx_on-canary_off-x86'
    # WARN: Don't use dashes.
    courses['win32']['plain'] = 'win{}.exe'
    courses['win32']['nop-slide'] = 'win{}.exe'
    target = courses[platform][course]
    try:
        real = target.format('x86' if bits == 32 else 'x64')
    except AttributeError as error:
        logging.error(error)
        raise ValueError('No such course!')
    else:
        return real


# TODO: Make it a class.
# TODO: Use other libaries.
def p32(addr):
    return unhexlify(addr[2:])[::-1]


def pause(message):
    try:
        input(message)
    except (KeyboardInterrupt, SyntaxError, EOFError):
        pass
