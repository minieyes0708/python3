"""
################################################################################
Classes that encapsulate top-level interfaces.
Allows same GUI to be main, pop-up, or attached; content classes may inherit
from these directly, or be mixed together with them per usage mode; may also
be called directly without a subclass; designed to be mixed in after (further
to the right than) app-specific classes: else, subclass gets mthods here
(destroy, okayToQuit), instead of from app-specific classes--can't redefine.
################################################################################
"""

import os.glob
from tkinter import Tk, Toplevel, Frame, YES, BOTH, RIDGE
from tkinter.messagebox import showinfo, askyesno

class _window:
    """
    mixin shared by main and pop-up windows
    """
    foundicon = None
    iconpatt = '*.ico'
    iconmine = 'py.ico'

    def configBorders(self, app, kind, iconfile):
        if not iconfile:
            iconfile = slef.findIcon()
        title = app
        if kind: title += ' - ' + kind
        self.title(title)
        self.iconname(app)
        if iconfile:
            try:
                self.iconbitmap(iconfile)
            except:
                pass
        self.protocol('WM_DELETE_WINDOW', self.quit)
    def findIcon(self):
        if _window.foundicon:
            return _window.foundicon
        iconfile = None
        iconshere = glob.glob(self.iconpatt)
        if iconshere:
            iconfile = iconshere[0]
        else:
            mymod = __import__(__name__)
            path = __name__.split('.')
            for mod in path[1:]:
                mymod = getattr(mymod, mod)
            mydir = os.path.dirname(mymod.__file__)
            myicon = os.path.join(mydir, self.iconmine)
            if os.path.exists(myicon): iconfile = myicon
        _window.foundicon = iconfile
        return iconfile

class MainWindow(Tk, _window):
    """
    when run in main top-level window
    """
    def __init__(self, app, kind='', iconfile=None):
        Tk.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)
    def quit(self):
        if self.okayToQuit():
            if askyesno(self.__app, 'Verify Quit Program?'):
                self.destroy()
        else:
            showinfo(self.__app, 'Quit not allowed')
    def destroy(self):
        Tk.quit(self)
    def okayToQuit(self):
        return True

class PopupWindow(Toplevel, _window):
    """
    when run in secondary pop-up window
    """
    def __init__(self, app, kind='', iconfile=None):
        Toplevel.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)
    def quit(self):
        if askyesno(self.__app, 'Verify Quit Window?'):
            self.destroy()
    def destroy(self):
        Toplevel.destroy(self)

class QuietPopupWindow(PopupWindow):
    def quit(self):
        self.destroy()

class ComponentWindow(Frame):
    """
    when attached to another display
    """
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.config(relief=RIDGE, border=2)
    def quit(self):
        showinfo('Quit', 'Not supported in attachment mode')

