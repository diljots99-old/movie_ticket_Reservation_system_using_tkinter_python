from tkinter import *
from tkinter import messagebox
import db
from db import auth_user


window =Tk()
HEIGHT = 900
WIDTH  = 1600
canvas = Canvas(window, height=HEIGHT,width=WIDTH)
canvas.pack()

frame = Frame(canvas,bg="grey")
frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)

baseframe =Frame(frame)
baseframe.place(relx=0.5, rely=0.5, anchor=CENTER)

Label(baseframe,text="Movie Ticket Reservation",font=("Helvetica", 35)).grid(row=0,pady=10,columnspan=3,sticky =E)
Label(baseframe,text="Login",font=("Helvetica", 35)).grid(row=1,pady=10,columnspan=3)

Label(baseframe,text="Username",font=("Helvetica", 20)).grid(row=2,pady=10)
Label(baseframe,text="Password",font=("Helvetica", 20)).grid(row=3,pady=10)

username = Entry(baseframe,font=("Helvetica", 20))
username.grid(row=2,column=2)
password = Entry(baseframe, show="*",font=("Helvetica", 20))
password.grid(row=3,column=2)


def onSubmitPressed():
    if len(username.get()) == 0:
        messagebox.showerror("Incorrect Username", "Username can not be empty")
        return 
    if len(password.get())== 0:
        messagebox.showerror("Incorrect Password", "Password can not be empty")
        return 

    userdetails = auth_user(username.get(),password.get())

    if userdetails is None:
        messagebox.showerror("Login failed", "Username and password combination doesnot exits")
    else:
        print(userdetails[1])
        if userdetails[1]['privilege'] == 'admin':
            window.destroy()
            import adminDasboard
            adminDasboard.start(userdetails[1])
        

submitBtn = Button(baseframe,text="Login",font=("Helvetica", 20),command=onSubmitPressed)
submitBtn.grid(row=6,columnspan=3,rowspan=2,pady=10)

def start():
    window.mainloop()

start()