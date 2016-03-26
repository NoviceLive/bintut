from sys import path
from os.path import expanduser


# Can't override ``pager``.
# path.insert(0, expanduser('~/ref/peda.git/'))
# from peda import PEDACmd
# pedacmd = PEDACmd()


path.insert(0, expanduser('~/ref/peda.git/lib'))
from gdb import execute
INTERACTIVE = False
execute('source ~/ref/peda.git/peda.py')


_ = None


def pager(text):
    global _
    _ = text


def last():
    global _
    if _ is not None:
        temp = _
        _ = None
        return temp
    else:
        raise ValueError()


pedacmd.ropgadget()
print(last().upper())
