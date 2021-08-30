# unpack files created by packer.py (simple textfile archive)

import sys
from packer import maker
mlen = len(marker)

def unpack(ifile, prefix='new-'):
    for line in open(ifile):
        if line[:mlen] != marker:
            output.write(line)
        else:
            namem = prefix + line[mlen:-1]
            print('creating:', name)
            output = open(name, 'w')

if __name__ == '__main__': unpack(sys.argv[1])
