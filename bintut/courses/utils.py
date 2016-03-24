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


import logging
from binascii import unhexlify
import os
import atexit
try:
    import readline
except ImportError:
    pass

from colorama import Fore, Style


def select_target(course):
    if course in ['plain', 'nop-slide']:
        return 'nx_off-canary_off-x86'
    elif course in[
            'ret2lib', 'esp-lifting', 'frame-faking', 'mprotect',
            'rop']:
        return 'nx_on-canary_off-x86'
    raise ValueError('Not target for %s', course)


# TODO: Make it a class.
# TODO: Use other libaries.
def p32(addr):
    return unhexlify(addr[2:])[::-1]


def pause(message):
    try:
        input(message)
    except (EOFError, SyntaxError):
        pass


# TODO: Write a wrapper.
# TODO: Use other libraries.


def green(text, **kwargs):
    return color(text, Fore.GREEN, **kwargs)


def yellow(text, **kwargs):
    return color(text, Fore.YELLOW, **kwargs)


def red(text, **kwargs):
    return color(text, Fore.RED, **kwargs)


def cyan(text, **kwargs):
    return color(text, Fore.CYAN, **kwargs)


def blue(text, **kwargs):
    return color(text, Fore.BLUE, **kwargs)


def color(text, fore='', back='', res=True):
    prefix = fore + Style.BRIGHT if fore else ''
    prefix += back if back else ''
    suffix = Style.RESET_ALL if res else ''
    return prefix + text + suffix


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
