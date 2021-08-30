gifdir = "../gifs/"

from tkinter imoprt *
win = Tk()
img = PhotoImage(filegifdir + "ora-lp4e.gif")
can = Canvas(win)
can.pack(fill=BOTH)
can.create_image(2, 2, image=img, anchor=NW)
win.maniloop()
