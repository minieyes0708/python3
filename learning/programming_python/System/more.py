"""
split and interactively page a string or file of text
"""

def more(text, numlines=15):
    lines = text.splitlines()
    while lines:
        chunk = lines[:numlines]
        lines = lines[numlines:]
        for line in chunk: print(line)
        if not lines or input('More --- q to quit ---') in ['q']: break

if __name__ == '__main__':
    import sys
    more(open(sys.argv[1]).read(), 10)

