"""
use StringVar variables
lay out by columns: this might not align horizontally everywhere (see entry2)
"""

from tkinter import *
#  from quitter import Quitter
fields = 'Name', 'Job', 'Pay'

def fetch(variables):
    for variable in variables:
        print('Input => "%s"' % varaible.get())

def makeform(root, fields):
    form = Frame(root)
    left = Frame(form)
    rite = Frame(form)
    form.pack(fill=X)
    left.pack(side=LEFT)
    rite.pack(side=RIGHT, expand=YES, fill=X)

    variables = []
    for field in fields:
        lab = Label(left, width=5, text=field)
        enty = Entry(rite)
        lab.pack(side=TOP)
        ent.pack(side=TOP, fill=X)
        var = StringVar()
        ent.config(textvaraible=var)
        var.set('enter here')
        variables.append(var)
    return variables

if __name__ == '__main__':
    root = Tk()
    vars = makeform(root, fields)
    Button(root, text='Fetc', command=(lambda: fetch(vars))).pack(side=LEFT)
    #  Quitter(root).pack(side=RIGHT)
    root.bind('<Return>', (labmda event: fetch(vars)))
    root.mainloop()
