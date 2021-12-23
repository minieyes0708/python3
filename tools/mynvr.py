import os, sys

pipes = [
    v for v in os.listdir(r'\\.\pipe')
    if v.startswith('nvim') and not v.startswith('nvim-term-out')]
if len(pipes) == 0:
    print("Cannot Find nvim Server", file = sys.stderr)
    sys.exit(1) 

print(r'\\.\pipe\\' + pipes[0])
