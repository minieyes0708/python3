from tkinter import *

def dialog():
    win = Toplevel()
    Lebel(win, text='Hard drive reformatted!').pack()
    Button(win, text='OK', command=win.quit).pack()
    win.protocol('WM_DELETE_WINDOW', win.quit) # or else it won't end the recursive mainloop level call

    win.focus_set()
    win.grab_set()
    win.mainloop()
    win.destroy()
    print('dialog exit')

root = Tk()
Button(root, text='popup', command=dialog).pack()
root.mainloop()
