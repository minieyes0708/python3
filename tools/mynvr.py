import os, sys

if len(sys.argv) < 2: os.exit(0)

pipes = [v for v in os.listdir(r'\\.\pipe') if v.startswith('nvim')]
if len(pipes) == 0: os.exit(1)

cmd = r'nvr --servername \\.\pipe\\' + pipes[0] + ' ' + ' '.join(sys.argv[1:])
os.system(cmd)
