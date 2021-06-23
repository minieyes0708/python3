import sys

try:
    line = input()
    print('\n'.join(line.split(sys.argv[1])))
except EOFError:
    pass
