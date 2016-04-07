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
from sys import exit
from time import sleep
from cmd import Cmd

from .init import LoggingMixIn, cyan, green, red, yellow


logging = getLogger(__name__)


def redisplay(debugger, burst, course=None, repl=True, target=None):
    debugger.clear()
    course = course if course else ''
    course += ' @ ' + target if target else ''
    if burst:
        print(red('==> Burst Mode: {}\n'.format(course)))
    else:
        print(yellow('==> Single Mode: {}\n'.format(course)))
    debugger.print_stack()
    debugger.print_reg()
    debugger.print_asm()
    if burst:
        sleep(burst)
    elif repl:
        try:
            print()
            REPL(debugger).cmdloop()
        except KeyboardInterrupt:
            exit(0)


class REPL(Cmd, LoggingMixIn):
    prompt = yellow('>>> ')

    def __init__(self, debugger):
        Cmd.__init__(self)
        self.debugger = debugger

    @staticmethod
    def do_EOF(dummy):
        return True

    @staticmethod
    def emptyline():
        return True

    def do_help(self, line):
        command = 'help {}'.format(line)
        try:
            output = self.debugger.execute(command)
        except Exception as error:
            self.logger.error(error)
        else:
            print(output)

    def do_redis(self, dummy):
        pass

    def default(self, line):
        try:
            output = self.debugger.execute(line)
        except Exception as error:
            self.logger.error(error)
        else:
            print(output)
