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
from binascii import hexlify

try:
    import gdb
except ImportError:
    pass
try:
    import pykd
except ImportError:
    pass
from colorama import Back

from .init import cyan, green, red, yellow
from .utils import LoggingMixin


# TODO: Add constraints.
class Debugger(object):
    def __new__(cls, environment, backend='gdb'):
        constructor = GDB if backend == 'gdb' else CDB
        return constructor(environment)


class GDB(LoggingMixin):
    def __init__(self, environment):
        LoggingMixin.__init__(self)
        self.gdb = gdb
        self.env = environment
        self.gdb.execute('set pagination off')
        self.gdb.execute('set disassembly-flavor intel')
        # TODO: Remove this for ASLR-bypassing courses.
        self.gdb.execute('set disable-randomization on')

    def execute(self, line):
        self.logger.debug('line: %s', line)
        output = self.gdb.execute(line, to_string=True)
        return output

    def start(self, filename, args):
        self.execute('file {}'.format(filename))
        self.execute('start {}'.format(' '.join(args)))

    def get_stack(self):
        wide = '32wx' if self.env.BITS == 32 else '16gx'
        command = 'x/{} ${}'.format(wide, self.env.SP)
        try:
            output = self.execute(command)
        except gdb.error:
            raise IOError()
        else:
            return output

    def get_pc_asm(self):
        command = 'x/i ${}'.format(self.env.IP)
        try:
            output = self.execute(command)
        except self.gdb.MemoryError as error:
            self.logger.debug('Original error: %s', error)
            addr = self.get_reg(self.env.SP)
            self.logger.debug('addr: %s', addr)
            pattern = error.args[0].split()[-1]
            self.logger.debug('pattern: %s', pattern)
            raise IOError(addr, pattern)
        else:
            return output

    def get_reg(self, name):
        command = 'info registers {}'.format(name)
        output = self.execute(command)
        return output.split()[-2]

    def step(self):
        command = 'stepi'
        self.execute(command)

    def next(self):
        command = 'nexti'
        self.execute(command)

    def cont(self):
        command = 'continue'
        self.execute(command)

    def clear(self):
        self.execute('shell clear')

    def print_stack(self):
        def repr_stack(stack, sp):
            for line in stack.splitlines():
                addr, values = line.split(':')
                values = ' '.join(values.split())
                if addr == sp:
                    print(Back.GREEN + red(addr, res=False),
                          yellow(values))
                else:
                    print(red(addr), cyan(values))
        try:
            stack = self.get_stack()
        except IOError as error:
            self.logger.error(error)
        else:
            repr_stack(stack, self.get_reg(self.env.SP))
            print()

    def print_reg(self):
        try:
            ip = self.get_reg(self.env.IP)
            sp = self.get_reg(self.env.SP)
            bp = self.get_reg(self.env.BP)
        except gdb.error as error:
            self.logger.error(error)
        else:
            print('{}: {} {}: {} {}: {}'.format(
                self.env.IP.upper(), red(ip),
                self.env.SP.upper(), yellow(sp),
                self.env.BP.upper(), cyan(bp)))
            print()

    def print_asm(self):
        def repr_asm(asm, pc):
            child = self.gdb.selected_inferior()
            mem = child.read_memory(asm['addr'], asm['length'])
            addr = hex(asm['addr']).strip('L')
            line = '{:25} {:25} {}'.format(
                cyan(addr, res=False),
                green(hexlify(mem).decode('utf-8'), res=False),
                red(asm['asm']), res=False)
            if asm['addr'] == pc:
                return Back.GREEN + line
            else:
                return line
        try:
            frame = self.gdb.selected_frame()
            arch = frame.architecture()
            ip = self.get_reg(self.env.IP)
            pc = int(ip, 16)
            asms = arch.disassemble(pc, pc+32)
        except (self.gdb.MemoryError, self.gdb.error) as error:
            self.logger.error(error)
        else:
            found = False
            for index, asm in enumerate(asms):
                if asm['addr'] == pc:
                    before = asms[index-8:index]
                    just = asms[index]
                    after = asms[index+1:index+1+8]
                    for one in before + [just] + after:
                        print(repr_asm(one, pc))
                    found = True
                    break
            if not found:
                raise RuntimeError('pc not found')


class CDB(LoggingMixin):
    def __init__(self, environment):
        LoggingMixin.__init__(self)
        self.pykd = pykd
        self.env = environment

    def execute(self, line):
        self.logger.debug('line: %s', line)
        output = self.pykd.dbgCommand(line)
        return output

    def start(self, filename, args):
        commandline = '{} {}'.format(filename, ' '.join(args))
        self.pykd.startProcess(commandline)
        from os.path import basename
        self.execute('bp {}!main'.format(basename(filename)))
        self.pykd.go()

    def get_stack(self):
        pass

    def get_pc_asm(self):
        self.logger.debug('ip: %s', self.get_reg(self.env.IP))
        try:
            output = self.pykd.disasm().opmnemo()
        except self.pykd.MemoryException as error:
            raise
        except self.pykd.DbgException as error:
            self.logger.error(error)
        else:
            return output

    def get_reg(self, name):
        return hex(self.pykd.reg(name))

    def step(self):
        self.pykd.trace()

    def next(self):
        self.pykd.step()

    def cont(self):
        self.pykd.go()

    def clear(self):
        from os import system
        system('cls')
