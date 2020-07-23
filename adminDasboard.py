from tkinter import *
from tkinter import messagebox
from db import auth_user


def start(userdetails={}):
    window =Tk()
    HEIGHT = 900
    WIDTH  = 1600
    canvas = Canvas(window, height=HEIGHT,width=WIDTH)
    canvas.pack()


    frame = Frame(canvas,bg="grey")
    frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
    print(userdetails)

    window.mainloop()
