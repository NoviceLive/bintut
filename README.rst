BinTut
======

Dynamic demonstration of the exploitation of
classical binary vulnerabilities.


Installation
============

``pip install bintut`` may or may not work for the time being.

Therefore it's recommended to just clone this repository
and run without installation
as long as necessary libraries are installed
by ``pip install -r requirements.txt``.


Requirements
------------

GDB_
++++

Python scripting support is required.

Pat_
++++

Customizable Lazy Exploit Pattern Utility.

Colorama_
+++++++++

Simple cross-platform colored terminal text in Python.

Click_
++++++

Python composable command line utility http://click.pocoo.org/.


Get Started
===========

See ``bintut --help`` and give a shot
via ``bintut --burst frame-faking``.

::

   bintut --help
   Usage: bintut [OPTIONS] [COURSE]

     Teach You A Binary Exploitation For Great Good.

   Options:
     -V, --version  Show the version and exit.
     -l, --list     List available courses.
     -6, --x64      Use x64 courses.
     -b, --burst    Turn on burst mode.
     -h, --help     Show this message and exit.


Available Courses
=================

`Stack-based buffer overflow`_
------------------------------

plain
+++++


`nop-slide`_
++++++++++++


ret2lib_
++++++++


frame-faking
++++++++++++


Bug Reports
===========

https://github.com/NoviceLive/bintut/issues.

BinTut is intended to be Python 2 compatible.

Bug reports are welcome.


References
==========

- `Smashing The Stack For Fun And Profit <http://phrack.org/issues/49/14.html>`_

- `Advanced return-into-lib(c) exploits (PaX case study) <http://phrack.org/issues/58/4.html>`_


.. _GDB: http://www.gnu.org/software/gdb/
.. _Pat: https://github.com/NoviceLive/pat
.. _Colorama: https://github.com/tartley/colorama
.. _Click: https://github.com/mitsuhiko/click
.. Stack-based buffer overflow: https://en.wikipedia.org/wiki/Stack_buffer_overflow
.. nop-slide: https://en.wikipedia.org/wiki/NOP_slide
.. ret2lib: https://en.wikipedia.org/wiki/Return-to-libc_attack
