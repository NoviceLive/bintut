#!/usr/bin/env python


from sys import argv

from elftools.elf.elffile import ELFFile
from elftools.elf.dynamic import DynamicSection


def main():
    for name in argv[1:]:
        with open(name, 'rb') as stream:
            elf = ELFFile(stream)
            for section in elf.iter_sections():
                if isinstance(section, DynamicSection):
                    for tag in section.iter_tags(type='DT_NEEDED'):
                        print(tag.entry, tag.needed)
                    break
            else:
                raise RuntimeError('Dynamic section not found.')


if __name__ == '__main__':
    main()
