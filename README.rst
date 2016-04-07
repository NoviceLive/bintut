BinTut
======


.. image:: https://img.shields.io/pypi/v/bintut.svg
   :target: https://pypi.python.org/pypi/BinTut


Dynamic or live demonstration of classical exploitation techniques
of typical memory corruption vulnerabilities,
from debugging to payload generation and exploitation,
for educational purposes :yum:.


What's BinTut
=============

BinTut is a set of tutorials, **as well as** exercises.


Tutorials
---------

See `Get Started`_ for usage information.

If you are a fan of Faiz_, ``Burst Mode`` or ``Single Mode`` should
sound familiar and inspiring.


Burst Mode
++++++++++

Watch and replay to obtain general understanding of the process.

Use ``-b / --burst`` to control the interval (in seconds).
Note that ``-b0`` means ``Single Mode``, which is the default.


Single Mode
+++++++++++

Play and examine various contents
such as the stack, registers or memory addresses,
carefully and step by step,
to acquire comprehensive and detailed knowledge of the process.

Use ``Enter`` or ``Ctrl + D`` to step.

You can execute normal GDB_ commands via the promt.
But note that BinTut won't synchronize the display
when you execute state-changing commands,
e.g. ``stepi`` or ``nexti``,
which are discouraged for the time being.

Another bad news is that readline_ does not work :scream:,
and I can't figure out the reason :scream:.


Exercises
---------

Write exploits that work outside debuggers
when you understand the principles and techniques
via watching and replaying (i.e. rewatching),
careful **playing** (i.e., **Single Mode**),
and most importantly,
**reading the source code responsible for exploit generation**,
which resides in a file named ``exploits.py``.


Installation
============

``pip install bintut`` may or may not work for the time being.

Therefore it's recommended to just clone this repository
and run without installation
as long as necessary libraries are installed
by ``pip install -r requirements.txt``.


Tested Platforms
----------------

`Arch Linux`_
+++++++++++++

Current version of `Arch Linux`_ ships GDB_ with Python 3,
in which I developed BinTut.

Version 0.2.1 should work fine.

Fedora_
+++++++

Fedora_ 23 Workstation comes with GDB_ with Python 3,
which has been tested
and BinTut version 0.2.1 is known to work properly
as in `Arch Linux`_.

- Install ``glibc.i686`` to support 32-bit programs if needed.

  ::

     sudo dnf install glibc.i686

- Install ``BinTut`` from PyPI.

  ::

     sudo pip3 install bintut

- Give it a try.

  ::

     bintut -b0.1 frame-faking

Debian_
+++++++

GDB_ from the stable branch of Debian_ ships with Python 2,
where BinTut 0.2.1 does not work.

Lastest source from Git works with minor problems.

- Add support to 32-bit programs if necessary.

  ::

     sudo dpkg --add-architecture i386
     sudo apt-get update
     sudo apt-get install libc6:i386

- Clone the lastest source code from Git and install requirements.

  ::

     git clone https://github.com/NoviceLive/bintut.git
     cd bintut
     sudo apt-get install python-pip
     pip2 install -r requirements.txt

- Run it without installation.

  ::

     python2 ./bintut.py -b0.1 frame-faking


Requirements
------------

GDB_
++++

Python scripting support is required.

BinTut is developed with Python 3,
but it's intended to be Python 2 compatible.

Therefore, when Python 2 yells at you,
feel free to create an issue or send me a pull request.

Known unresolved issues existing on Python 2
********************************************

- Can't display disassembly after returning to shellcode.

- Can't print the payload for some courses.


Ropper_
+++++++

Show information about binary files and find gadgets to
build rop chains for different architectures.

pyelftools_
+++++++++++

Python library for analyzing ELF files
and DWARF debugging information.

Pat_
++++

Customizable Lazy Exploit Pattern Utility.

Colorama_
+++++++++

Simple cross-platform colored terminal text in Python.

Click_
++++++

Python composable command line utility.


.. _`Get Started`:

Get Started
===========

See ``bintut --help`` and give it a shot
via ``bintut --burst 0.1 frame-faking``.

::

   ./bintut.py --help
   Usage: bintut.py [OPTIONS] [COURSE]

     Teach You A Binary Exploitation For Great Good.

   Options:
     -V, --version      Show the version and exit.
     -l, --list         List available courses.
     -6, --x64          Use x64 courses.
     -A, --aslr         Enable ASLR.
     -b, --burst FLOAT  Use this burst mode interval.  [default: 0]
     -v, --verbose      Be verbose.
     -q, --quiet        Be quiet.
     -h, --help         Show this message and exit.


Available Courses
=================

Other courses might be added later.


`Stack-based buffer overflow`_
------------------------------

1. plain
++++++++

Return to plain shellcode.

Linux x86 / x64.

NX: Disabled.

ASLR: Disabled.

Stack Protector: Disabled.


2. `nop-slide`_
+++++++++++++++

Return to NOPs plus shellcode.

Linux x86 / x64.

NX: Disabled.

ASLR: Disabled.

Stack Protector: Disabled.

This course is not demonstrative enough
and shall be updated when the author finds a scenario
where `nop-slide`_ really stands out.


3. jmp-esp
++++++++++

Return to shellcode via JMP ESP / RSP.

Linux x86 / x64.

NX: Disabled.

ASLR: Disabled.

Stack Protector: Disabled.


4. ret2lib_
+++++++++++

Return to functions.

Linux x86.

NX: **Enabled**.

ASLR: Disabled.

Stack Protector: Disabled.

.. _`Notes for x64`:

Notes for x64
*************

Either on Linux or Windows, the `ABI of x64`_, unlike that of x86,
passes some arguments, first six or four integral arguments
on Linux or Windows respectively,
via registers, which may not be controlled
without resort to certain gadgets.

Therefore, it may be discussed in the section for ROP_.


5. frame-faking
+++++++++++++++

Return to chained functions via LEAVE RET gadget.

Linux x86.

NX: **Enabled**.

ASLR: Disabled.

Stack Protector: Disabled.


Notes for x64
*************

See `Notes for x64`_.


Bug Reports
===========

Create `issues <https://github.com/NoviceLive/bintut/issues>`_.

BinTut may or may not work on your system,
but bug reports with necessary information are always welcome.


References
==========

- `Smashing The Stack For Fun And Profit <http://phrack.org/issues/49/14.html>`_

- `Advanced return-into-lib(c) exploits (PaX case study) <http://phrack.org/issues/58/4.html>`_


.. _Arch Linux: https://www.archlinux.org/
.. _Fedora: https://getfedora.org/
.. _Debian: https://www.debian.org/

.. _GDB: http://www.gnu.org/software/gdb/
.. _Ropper: https://github.com/sashs/Ropper
.. _pyelftools: https://github.com/eliben/pyelftools
.. _Pat: https://github.com/NoviceLive/pat
.. _Colorama: https://github.com/tartley/colorama
.. _Click: https://github.com/mitsuhiko/click

.. _Stack-based buffer overflow: https://en.wikipedia.org/wiki/Stack_buffer_overflow
.. _nop-slide: https://en.wikipedia.org/wiki/NOP_slide
.. _ret2lib: https://en.wikipedia.org/wiki/Return-to-libc_attack
.. _ROP: https://en.wikipedia.org/wiki/Return-oriented_programming
.. _ABI of x64: https://en.wikipedia.org/wiki/X86_calling_conventions#x86-64_calling_conventions
.. _readline: https://docs.python.org/3/library/readline.html
.. _Faiz: https://en.wikipedia.org/wiki/Kamen_Rider_555
