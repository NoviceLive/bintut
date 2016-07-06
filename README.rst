BinTut
@@@@@@


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

Notice
------

If pip_ is used to install BinTut,
make sure that you use the pip_ version
corresponding to the Python_ version shipped with GDB_.
For more details, see `#1`_.

``pip install bintut`` may or may not work for the time being.

Therefore it's recommended to just clone this repository
and run without installation
as long as necessary libraries are installed
by ``pip install -r requirements.txt``.

Warning
-------

BinTut does not work inside virtualenv at present.

Tested Platforms
----------------

`Arch GNU/Linux`_
+++++++++++++++++

Current version of `Arch GNU/Linux`_ ships GDB_ with Python_ 3,
in which I developed BinTut.

The latest release version should work fine.

- Enable ``multilib`` in ``/etc/pacman.conf``.

- Install ``gcc-mulitilib`` to support compiling and execution of 32-bit programs.

  ::

     sudo pacman -S gcc-mulitilib

- Install Python_ 3 and ``pip3``.

  ::

     sudo pacman -S python python-pip

- Install BinTut using ``pip3``

  ::

     sudo pip3 install bintut

- You are ready!

  ::

     bintut -b0.1 jmp-esp

`Fedora GNU/Linux`_
+++++++++++++++++++

The latest Fedora Workstation comes with GDB_ with Python_ 3,
which has been tested
and BinTut is known to work properly
as in `Arch GNU/Linux`_.

- Install ``glibc.i686`` to support 32-bit programs if needed.

  ::

     sudo dnf install glibc.i686

- Install ``BinTut`` from PyPI.

  ::

     sudo pip3 install bintut

- Give it a try.

  ::

     bintut -b0.1 frame-faking

`Debian GNU/Linux`_
+++++++++++++++++++

GDB_ from the stable branch of `Debian GNU/Linux`_ ships with Python_ 2.

Latest source from Git works with minor problems.

- Add support to 32-bit programs if necessary.

  ::

     sudo dpkg --add-architecture i386
     sudo apt-get update
     sudo apt-get install libc6:i386

- Clone the latest source code from Git and install requirements.

  ::

     git clone https://github.com/NoviceLive/bintut.git
     cd bintut
     sudo apt-get install python-pip gdb
     pip2 install -r requirements.txt

- Run it without installation.

  ::

     python2 ./bintut.py -b0.1 frame-faking


`Kali GNU/Linux`_
+++++++++++++++++

GDB_ from the latest rolling version of `Kali GNU/Linux`_ ships with Python_ 3.

- Enable ``i386`` support according to aforementioned instructions.

- Install ``pip3``

  ::

     apt-get install python3-pip

- Install the latest BinTut release using ``pip3``

  ::

     pip3 install bintut

- Start hacking!

  ::

     bintut -b0.1 jmp-esp


Requirements
------------

GDB_
++++

Python_ scripting support is required.

BinTut is developed with Python_ 3,
but it's intended to be Python_ 2 compatible.

Therefore, when Python_ 2 yells at you,
feel free to create an issue or send me a pull request.

Known unresolved issues existing on Python_ 2
*********************************************

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

4. off-by-one NULL
++++++++++++++++++

Variant of ``plain`` `stack-based buffer overflow`_.

Linux x86 / x64.

NX: Disabled.

ASLR: Disabled.

Stack Protector: Disabled.

5. ret2lib_
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

6. frame-faking
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

BinTut might or might not work on your system,
but bug reports with necessary information are always welcome.

Tips
----

Remember to include ``bintut --version`` in your report.

You can just submit the verbose log (``stderr``) if out of words,
e.g., ``bintut -v -b0.1 frame-faking 2>log.txt``.


TODO List & You Can Contribute
==============================

- Improve the code if you find something that can be done better.

  The codebase of BinTut can always be improved by those
  who have a deeper understanding of Python than the author.

  Also, there are hardcoded behaviors which can be generalized.

- Change color scheme to red highlight when content changes.

  Currently, our color scheme remains unchanged,
  in predefined colors,
  which is just not eye-catching or obvious
  when we want to observe some significant changes
  in certain registers or specific memory locations.

  Here is an example of such change,
  the least-significant-**byte** of saved EBP / RBP
  being cleared due to an off-by-one NULL write.

  Ref. That's what you will expect in OllyDbg
  and probably many other debuggers will also behave in this manner.

  Ref. Some GDB_ enhancement projects have already implemented this.

- Synchronize the display when executing state-changing commands.

- Add course variants that does not allow NULL bytes.

  For example, add variant courses
  using ``strcpy`` instead of ``fread`` to trigger overflow,
  in order to demonstrate the techniques
  to survive in severe environments,
  which happen to be the case of our real world.

- Use a better combination of chained functions for ``frame-faking``.

  What follows is the current choice.

  Yes, two consecutive ``/bin/sh`` and ``exit``.

  ::

     elif post == 'frame-faking':
         payload = (
             Faked(offset=offset, address=addr) +
             Faked(b'system', ['/bin/sh']) +
             Faked(b'execl', ['/bin/sh', '/bin/sh', 0]) +
             Faked(b'exit', [0]))

- Support demonstration on Windows and MacOS.


References
==========

- `Smashing The Stack For Fun And Profit <http://phrack.org/issues/49/14.html#article>`_
- `The Frame Pointer Overwrite <http://phrack.org/issues/55/8.html#article>`_
- `Advanced return-into-lib(c) exploits (PaX case study) <http://phrack.org/issues/58/4.html#article>`_


.. _Arch GNU/Linux: https://www.archlinux.org/
.. _Fedora GNU/Linux: https://getfedora.org/
.. _Debian GNU/Linux: https://www.debian.org/
.. _Kali GNU/Linux: https://www.kali.org/

.. _pip: https://pip.pypa.io/
.. _Python: https://www.python.org/
.. _Capstone: http://www.capstone-engine.org/
.. _filebytes: https://github.com/sashs/filebytes
.. _#1: https://github.com/NoviceLive/bintut/issues/1

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
