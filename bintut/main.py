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
from sys import exit
from subprocess import check_call, CalledProcessError
from os.path import join
from collections import OrderedDict

import click
from pkg_resources import resource_filename

from . import VERSION_PROMPT, PROGRAM_NAME
from .courses.utils import simple_platform


@click.command(
    context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(VERSION_PROMPT,
                      '-V', '--version', prog_name=PROGRAM_NAME)
@click.option('-l', '--list', 'list_courses', is_flag=True,
              help='List available courses.')
@click.option('-6', '--x64', is_flag=True,
              help='Use x64 courses.')
@click.option('-A', '--aslr', is_flag=True,
              help='Enable ASLR.')
@click.option('-b', '--burst',
              type=float, default=0, show_default=True,
              help='Use this burst mode interval.')
@click.argument('course', required=False)
@click.option('-v', '--verbose', count=True, help='Be verbose.')
@click.option('-q', '--quiet', count=True, help='Be quiet.')
def main(course, list_courses, x64, aslr, burst, quiet, verbose):
    """Teach You A Binary Exploitation For Great Good."""
    courses = make_courses()
    if list_courses:
        print('Available Courses:\n')
        for course in courses:
            print('{:16} {}'.format(course, courses[course]))
    elif course:
        level = logging.INFO + (quiet-verbose)*10
        if course not in courses:
            print('No Such Courses!')
            exit(1)
        bits = 64 if x64 else 32
        path = resource_filename(__name__, '')
        platform = simple_platform()
        logging.debug('platform: %s', platform)
        if platform == 'linux':
            entry = join(path, 'entry.py')
            commandline = [
                'gdb', '--quiet', '--batch',
                '--eval-command', 'pi burst={}'.format(burst),
                '--eval-command', 'pi course="{}"'.format(course),
                '--eval-command', 'pi aslr={}'.format(aslr),
                '--eval-command', 'pi bits={}'.format(bits),
                '--eval-command', 'pi level={}'.format(level),
                '--eval-command', 'source {}'.format(entry)]
            try:
                check_call(commandline)
            except CalledProcessError:
                exit(1)
        else:
            from .courses.main import start_tutor
            start_tutor(course, bits, burst, level)
    exit(0)


def make_courses():
    courses = OrderedDict()
    courses.update({
        'plain': 'Return to plain shellcode. (Linux x86 / x64.)'})
    courses.update({
        'nop-slide':
        'Return to NOPs plus shellcode. (Linux x86 / x64.)'})
    courses.update({
        'jmp-esp':
        'Return to shellcode via JMP ESP / RSP. (Linux x86 / x64.)'})
    courses.update({
        'ret2lib': 'Return to functions. (Linux x86.)'})
    courses.update({
        'frame-faking':
        'Return to chained functions via LEAVE RET. (Linux x86.)'})
    courses.update({
        'off-by-one':
        'off-by-one NULL write stack overflow. (Linux x86 / x64.)'})
    return courses
