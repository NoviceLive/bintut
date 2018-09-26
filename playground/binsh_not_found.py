#! /usr/bin/env python3


"""
$ bintut -b0.3 ret2lib

... skipped ...

Traceback (most recent call last):
  File "/home/blind7/safe/trustworthy/public-repo/bintut.git/bintut/entry.py", line 56, in <module>
    start_tutor(course, bits, burst, aslr, level)
  File "/home/blind7/safe/trustworthy/public-repo/bintut.git/bintut/courses/main.py", line 72, in start_tutor
    payload = make_payload(offset, addr, course)
  File "/home/blind7/safe/trustworthy/public-repo/bintut.git/bintut/courses/exploits.py", line 42, in make_payload
    payload = Fill(offset) + Ret2Fun()
  File "/home/blind7/safe/trustworthy/public-repo/bintut.git/bintut/courses/exploits.py", line 120, in __add__
    return Payload(self.compose() + other.compose())
  File "/home/blind7/safe/trustworthy/public-repo/bintut.git/bintut/courses/exploits.py", line 200, in compose
    binsh = resolver.get('/bin/sh')
  File "/home/blind7/safe/trustworthy/public-repo/bintut.git/bintut/courses/exploits.py", line 309, in get
    return self.get_bin_sh_address()
  File "/home/blind7/safe/trustworthy/public-repo/bintut.git/bintut/courses/exploits.py", line 351, in get_bin_sh_address
    raise RuntimeError('Failed to find /bin/sh!')
RuntimeError: Failed to find /bin/sh!
"""


from binascii import hexlify
from shutil import which

from ropper import Loader, Ropper


if __name__ == '__main__':
    # Arch:   /usr/lib32/libc-2.28.so
    # Fedora: /usr/lib/libc-2.26.so
    libc = Loader.open('/usr/lib32/libc.so.6' if which('pacman') else '/lib/libc.so.6')
    ropper = Ropper()

    code = hexlify(b'/bin/sh').decode('utf-8')
    print(code)

    opcode, size = ropper._formatOpcodeString(code)
    for sec in libc.executableSections + libc.dataSections:
        print(sec.name, ropper._searchOpcode(sec, libc, opcode, size))
