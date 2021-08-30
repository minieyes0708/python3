"""
################################################################################
tools launcher; uses guimaker templates, guimixin std quit dialog;
I am just a class library: run mytools script to display the GUI;
################################################################################
"""

from tkinter import *
from learning.programming_python.GUI.Tools.guimixin import GuiMixin
from learning.programming_python.GUI.Tools.guimaker import *

class ShellGui(GuiMixin, GuiMakerWindowMenu):
    def start(self):
        self.setMenuBar()
        self.setToolBar()
        self.master.title("Shell Tools Listbox")
        self.master.iconname("Shell Tools")
    def handleList(self, event):
        label = self.listbox.get(ACTIVE)
        self.runCommand(label)
    def makeWidgets(self):
        sbar = Scrollbar(self)
        list = Listbox(self, bg='white')
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        for (label, action) in self.fetchCommands():
            list.insert(END, label)
        list.bind('<Double-1>', self.handleList)
        self.listbox = list
    def forToolBar(self, label):
        return True
    def setToolBar(self):
        self.toolBar = []
        for (label, action) in self.fetchCommands():
            if self.fotToolBar(label):
                self.toolBar.append((label, action, dict(side=LEFT)))
        self.toolBar.append(('Quit', self.quit, dict(side=RIGHT)))
    def setMenuBar(self):
        toolEntries = []
        self.menuBar = [
                ('File', 0, [('Quit', -1, self.quit)]),
                ('Tools', 0, toolEntries)
                ]
        for (label, action) in self.fetchCommands():
            toolEntries.append((label, -1, action))

################################################################################
# delegate to template type-specific subclasses
# which delegate to app tool-set-specific subclasses
################################################################################

class ListMenuGui(ShellGui):
    def fetchCommands(self):
        return self.myMenu
    def runCommand(self, cmd):
        for (label, action) in self.myMenu:
            if label == cmd: action()

class DictMenuGui(ShellGui):
    def fetchCommands(self):
        return self.myMenu.items()
    def runCommand(self, cmd):
        self.myMenu[cmd]()
