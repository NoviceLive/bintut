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

from .init import LoggingMixIn, cyan, green, red, yellow

logging = getLogger(__name__)


def align_32(addr):
    logging.debug('addr: %s', addr)
    return '{:#010x}'.format(int(addr, 16)) if addr else ''


def align_64(addr):
    logging.debug('addr: %s', addr)
    return '{:#018x}'.format(int(addr, 16)) if addr else ''


# TODO: Abstract them.
class Debugger(object):
    def __new__(cls, environment, backend='gdb'):
        constructor = GDB if backend == 'gdb' else CDB
        return constructor(environment)


class GDB(LoggingMixIn):
    def __init__(self, environment):
        self.gdb = gdb
        self.env = environment
        self.gdb.execute('set pagination off')
        self.gdb.execute('set disassembly-flavor intel')
        if self.env.ASLR:
            self.gdb.execute('set disable-randomization off')
        else:
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
            sp = self.get_reg(self.env.SP)
            pattern = error.args[0].split()[-1]
            self.logger.debug('sp: %s pattern: %s', sp, pattern)
            raise IOError(sp, pattern)
        else:
            return output

    def get_reg(self, name):
        command = 'info registers {}'.format(name)
        try:
            output = self.execute(command)
        except gdb.error as error:
            self.logger.error(error)
            return None
        else:
            return output.split()[-2]

    def step(self):
        command = 'stepi'
        try:
            self.execute(command)
        except self.gdb.MemoryError as error:
            self.logger.error(error)
            raise IOError

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
                values = values.split()
                if addr == sp:
                    top = values[0]
                    rest = ' '.join(values[1:])
                    line = '==> {} {} {}'.format(
                        red(addr), red(top, back='green'),
                        yellow(rest))
                else:
                    line = '    {} {}'.format(
                        red(addr), cyan(' '.join(values)))
                print(line)
        try:
            stack = self.get_stack()
        except IOError as error:
            self.logger.error(error)
        else:
            repr_stack(stack, self.get_reg(self.env.SP))
            print()

    def print_reg(self):
        def print_regs(regs, colors):
            values = [self.get_reg(reg) for reg in regs]
            line = []
            for reg, value in zip(regs, values):
                if self.env.BITS == 32:
                    value = align_32(value)
                else:
                    value = align_64(value)
                value = colors[reg](value)
                line.append('{}: {}'.format(reg.upper(), value))
            print('    '.join(line))
        colors = [red, yellow, cyan]
        regs = [self.env.CX, self.env.DX, self.env.BX]
        print_regs(regs, dict(zip(regs, colors)))
        regs = [self.env.AX, self.env.SI, self.env.DI]
        print_regs(regs, dict(zip(regs, colors)))
        regs = [self.env.IP, self.env.SP, self.env.BP]
        print_regs(regs, dict(zip(regs, colors)))
        print()

    def print_asm(self):
        def repr_asm(name, head, asm, pc):
            child = self.gdb.selected_inferior()
            mem = child.read_memory(asm['addr'], asm['length'])
            addr = hex(asm['addr']).strip('L')
            if name:
                delta = asm['addr'] - int(head, 16)
                delta = '<{}+{}>'.format(name, delta)
                fmt = '    {:20} {:24} {:25} {}'
            else:
                delta = ''
                fmt = '    {:36}{}{:25} {}'
            line = fmt.format(
                cyan(addr, res=False), yellow(delta, res=False),
                green(hexlify(mem).decode('utf-8'), res=False),
                red(asm['asm']), res=False)
            if asm['addr'] == pc:
                return Back.GREEN + '==> ' + line.strip()
            else:
                return line
        try:
            ip = self.get_reg(self.env.IP)
            self.logger.debug('ip: %s', ip)
            pc = int(ip, 16)
            self.logger.debug('pc: %s', pc)
        except TypeError as error:
            self.logger.error(error)
        try:
            frame = self.gdb.selected_frame()
            self.logger.debug('frame: %s', frame)
            name = frame.name()
            if name:
                head = self.execute('p {}'.format(name)).split()[-2]
            else:
                head = None
            self.logger.debug('name: %s head: %s', name, head)
            arch = frame.architecture()
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
                        print(repr_asm(name, head, one, pc))
                    found = True
                    break
            if not found:
                raise RuntimeError('pc not found')


class CDB(LoggingMixIn):
    def __init__(self, environment):
        self.pykd = pykd
        self.env = environment

    def execute(self, line):
        self.logger.debug('line: %s', line)
        # TODO: Write special handlers for state-changing commands.
        if line == 'go':
            self.pykd.go()
        else:
            output = self.pykd.dbgCommand(line)
            return output
        return None

    def start(self, filename, args):
        try:
            self.pykd.detachProcess()
        except RuntimeError:
            pass
        commandline = '{} {}'.format(filename, ' '.join(args))
        self.pykd.startProcess(commandline)
        from os.path import basename, splitext
        base = splitext(basename(filename))[0]
        self.execute('bp {}!main'.format(base))
        # TODO: Find a better way.
        self.pykd.go()
        self.pykd.go()

    def get_stack(self):
        pass

    def get_pc_asm(self):
        self.logger.debug('ip: %s', self.get_reg(self.env.IP))
        try:
            output = self.pykd.disasm().opmnemo()
        except self.pykd.DbgException as error:
            self.logger.error('Original error: %s', error)
            pattern = self.get_reg(self.env.IP)
            sp = self.get_reg(self.env.SP)
            self.logger.debug('sp: %s pattern: %s', sp, pattern)
            raise IOError(sp, pattern)
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

    def print_stack(self):
        command = 'dd {}-0x40'.format(self.env.SP)
        try:
            values = self.execute(command)
        except self.pykd.DbgException as error:
            self.logger.error(error)
        else:
            sp = self.pykd.reg(self.env.SP)
            for line in values.splitlines():
                if int(line.split()[0], 16) == sp:
                    print(red(line))
                else:
                    print(cyan(line))

    def print_reg(self):
        try:
            ip = hex(self.pykd.getIP()).strip('L')
            sp = hex(self.pykd.getSP())
            bp = self.get_reg(self.env.BP)
        except self.pykd.DbgException as error:
            self.logger.error(error)
        else:
            print('{}: {} {}: {} {}: {}'.format(
                self.env.IP.upper(), red(ip),
                self.env.SP.upper(), yellow(sp),
                self.env.BP.upper(), cyan(bp)))

    def print_asm(self):
        command = 'u {} l10'.format(self.env.IP)
        try:
            asms = self.execute(command)
        except self.pykd.DbgException as error:
            self.logger.error(error)
        else:
            ip = self.pykd.reg(self.env.IP)
            for line in asms.splitlines()[1:]:
                try:
                    address, opcode, ins = line.split(None, 2)
                except ValueError as error:
                    print(red('{}: {}'.format(line, error)))
                else:
                    line = '{:25} {:25} {}'.format(
                        cyan(address, res=False),
                        yellow(opcode, res=False), red(ins))
                    if int(address, 16) == ip:
                        print(Back.GREEN + line)
                    else:
                        print(line)
