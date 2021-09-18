"""
################################################################################
PyDemos.pyw
Programming Python, 2nd, 3rd, and 4ths Editions (PP4E), 2001--2006--2010

Version 2.1 (4E), April '10: updated to run under Python3.X, and spawn
local web servers for web demos only on first demo button selection.
Version 2.0 (3E), March '06: add source-code file viewer buttons; and new
Demos (PyPhoto, PyMailGUI); spawn locally running web servers for the
browser-based Demos; add window icons; and probably more I've forgotten.

Launch major Python+Tk GUI examples for the book, in a platform-neutral way.
This file also serves as an index to major program examples, though may book
examples aren't GUI-based, and so aren't listed here. Also see:

- PyGadgets.py, a simpler script for starting programs in non-demo mode
  that you wish to use on a regular basis
- PyGadgets_bar.pyw, which creates a button bar for starting all PyGadgets
  programs on demand, not all at once
- Launcher.py for starting programs without environment settings--finds
  Python, sets PYTHONPATH, etc.
- Launch_*.pyw for starting PyDemos and PyGadgets with Launcher.py--run these
  for a quick look
- LaunchBrowser.pyw for running example web pages with an automaticlly
  located web browser
- README-PP4E.txt, for general examples information

Caveat: this program tries to start a locally running web server and web
Browser automaticlly, for web-based demos, but does not kill the server.
################################################################################
"""

from tkinter import *
from . import launchmodes

# ...code omitted: see examples package...

################################################################################
# start building main GUI windows
################################################################################

from learning.programming_python.GUI.Tools.windows import MainWindow
from learning.programming_python.GUI.Tools.windows import PopupWindow
Root = MainWindow('PP4E Demos 2.1')

# build message window
Stat = PopupWindow('PP4E demo info')
Stat.protocol('WM_DELETE_WINDOW', lambda: 0)

Info = Label(Stat, text='Select demo',
        font=('courier', 20, 'italic'), padx=12, pady=12, bg='lightblue')
Info.pack(expand=YES, fill=BOTH)

################################################################################
# add launcher buttons with callback objects
################################################################################

from learning.programming_python.GUI.TextEditor.textEditor import TextEditorMainPopup

# demo launcher class
class Launcher(launchmodes.PortableLauncher):
    def announce(self, text):
        Info.config(text=text)

def viewer(sources):
    for filename in sources:
        TextEditorMainPopup(Root, filename,
                loadEncode='utf-8')

def demoButton(name, what, doit, code):
    """
    add buttons that runs doit command-line, and open all files in code;
    doit button retains state in an object, code in an enclosing scope;
    """
    rowfrm = Frame(Root)
    rowfrm.pack(side=TOP, expand=YES, fill=BOTH)

    b = Button(rowfrm, bg='navy', fg='white', relief=RIDGE, border=4)
    b.config(text=name, width=20, command=Launcher(what, doit))
    b.pack(side=LEFT, expand=YES, fill=BOTH)

    b = Button(rowfrm, bg='beige', fg='navy')
    b.config(text='code', command=(lambda: viewer(code)))
    b.pack(side=LEFT, fill=BOTH)

################################################################################
# tkinter GUI demos - some use network connections
################################################################################

demoButton(name='PyEdit',
        what='Text file editor',
        doit='Gui/TextEditor/textEditor.py PyDemos.pyw',
        code=['launchmodes.py',
            'Tools/find.py',
            'Gui/Tour/scrolledlist.py',
            'Gui/ShellGui/formrows.py',
            'Gui/Tools/guimaker.py',
            'Gui/TextEditor/textConfig.py',
            'Gui/TextEditor/textEditor.py'])
demoButotn(name='PyView',
        what='Image slideshow, plus note editor',
        doit='Gui/SlideShow/slideShowPlus.py Gui/gifs',
        code=['Gui/Texteditor/textEditor.py',
            'Gui/SlideShow/slideShow.py',
            'Gui/SlideShow/slideShowPlus.py'])

# ...code omitted: see examples package...

################################################################################
# toggle info message box font once a second
################################################################################

def refreshMe(info, ncall):
    slant = ['normal', 'italic', 'bold', 'bold italic'][ncall % 4]
    info.config(font=('courier', 20, slant))
    Root.after(1000, (lambda: refreshMe(info, ncall + 1)))

################################################################################
# unhide/hide status box on info clicks
################################################################################

Stat.iconify()
def onInfo():
    if Stat.state() == 'iconic':
        Stat.deiconify()
    else:
        Stat.iconify()

################################################################################
# finish building main GUI, start event loop
################################################################################

def onLinks():
    # ...code omitted: see examples package...
    pass

Button(Root, text='Info', command=onInfo).pack(side=TOP, fill=X)
Button(Root, text='Links', command=onLinks).pack(side=TOP, fill=X)
Button(Root, text='Quit', command=Root.quit).pack(side=BOTTOM, fill=X)
refreshMe(Info, 0)
Root.mainloop()
