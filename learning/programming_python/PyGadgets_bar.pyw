"""
run a PyGadgets toolbar only, instead of starting all the gadgets immediately;
filename avoids DOS pop up on Widnows: rename to '.py' to see console messages;
"""

from . import PyGadgets
PyGadgets.runLauncher(PyGadgets.mytools)
