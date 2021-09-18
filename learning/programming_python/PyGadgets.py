"""
################################################################################
Start various examples; run me at start time to make them always available.
This file is meat for starting programs you actually wish to use; see
PyDemos for starting Python/Tk demos and more details on program start
options. Windows usage note: this is a '.py' to show messages in a console
window when run or clicked (including a 10 second pause to make sure it's
visible whilte gadgets start if clicked). To avoid Windows concole pop up,
run with the 'pythonw' program (not 'python'), rename to '.pyw' suffix,
mark with 'run minimized' window property, or spawn elsewhere (see PyDemos).
################################################################################
"""

import sys, time, time
from tkinter import *
from .launchmodes import PortableLauncher
from .GUI.Tools.windows import MainWindow

def runImmediate(mytools):
    """
    launch gadget programs immediately
    """
    print('Starting Python/Tk gadgets...')
    for (name, commandLine) in mytools:
        PortableLauncher(name, commandLine)()
    print('One moment please...')
    if sys.platform[:3] == 'win':
        for i in range(10):
            time.sleep(1); print('.' * 5 * (i + 1))

def runLauncher(mytools):
    """
    pop up a simple launcher bar for later use
    """
    root = MainWindow('PyGadgets PP4E')
    for (name, commandLine) in mytools:
        b = Button(root, text=name, fg='black', bg='beige', border=2,
                command=PortableLauncher(name, commandLine))
        b.pack(side=LEFT, expand=YES, fill=BOTH)
    root.mainloop()

mytools = [
        ('PyEdit', 'Gui/TextEditor/textEditor.py'),
        ('PyCalc', 'Lang/Calculator/calculator.py'),
        ('PyPhoto', 'Gui/PIL/pyphoto1.py Gui/PIL/images'),
        ('PyMail', 'Internet/Email/PyMailGui/PyMailGui.py'),
        ('PyClock', 'Gui/Clock/clock.py -size 175 -bg white'
            ' -picture Gui/gifs/pythonPowered.gif'),
        ('PyToe', 'Ai/TicTacToe/tictactoe.py'
            ' -mode Minimax -fg white -bg navy'),
        ('PyWeb', 'LaunchBrowser.pyw'
            ' -live index.html learning-python.com')]
        # ' -live PyInternetDemos.html localhost:80')]
        # ' -file')] # PyInternetDemos assumes local server started

if __name__ == "__main__":
    prestart, toolbar = True, False
    if prestart:
        runImmediate(mytools)
    if toolbar:
        runLauncher(mytools)
