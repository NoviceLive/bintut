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
from sys import platform
import os
import atexit
try:
    import readline
except ImportError:
    pass
from collections import defaultdict


logging = getLogger(__name__)


def simple_platform():
    """Fuck."""
    if platform in ['linux', 'linux2']:
        return 'linux'
    elif platform in ['win32']:
        return 'win32'
    else:
        raise ValueError('Unknow platform: {}'.format(platform))


def tree():
    return defaultdict(tree)


# TODO: Use other methods.
class LoggingMixin(object):
    def __init__(self):
        from logging import getLogger
        self.logger = getLogger(self.__class__.__name__)


# TODO: Find a better way and group with ``bintut -l``.
def select_target(course, platform, bits):
    logging.debug('course: %s', course)
    logging.debug('platform: %s', platform)
    logging.debug('bits: %s', bits)
    if bits == 64 and course in ['ret2lib', 'frame-faking']:
        raise ValueError('Course only available in x86!')
    courses = tree()
    courses['linux']['plain'] = 'nx_off-canary_off-{}'
    courses['linux']['nop-slide'] = 'nx_off-canary_off-{}'
    courses['linux']['ret2lib'] = 'nx_on-canary_off-x86'
    courses['linux']['frame-faking'] = 'nx_on-canary_off-x86'
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


# TODO: Support line editing.
def setup_read_line(history_dir='.'):
    """Setup readline.

    For input on Python 3 and raw_input on Python 2.
    """
    history = os.path.join(history_dir, 'history')
    try:
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode emacs')
    except NameError:
        pass
    try:
        readline.read_history_file(history)
    except (NameError, OSError):
        pass
    if os.path.isdir(history_dir):
        atexit.register(readline.write_history_file, history)
    else:
        logging.warning('history saving unavailable.')
