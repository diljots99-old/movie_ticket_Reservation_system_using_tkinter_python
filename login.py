from tkinter import *
from tkinter import messagebox
import db
from db import auth_user

class  Login(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.onCreate()
      


    def onCreate(self):

        HEIGHT = 900
        WIDTH  = 1600
        self.canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        self.canvas.pack()

        self.frame = Frame(self.canvas,bg="grey")
        self.frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)

        self.baseframe =Frame(self.frame)
        self.baseframe.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.baseframe,text="Movie Ticket Reservation",font=("Helvetica", 35)).grid(row=0,pady=10,columnspan=3,sticky =E)
        Label(self.baseframe,text="Login",font=("Helvetica", 35)).grid(row=1,pady=10,columnspan=3)

        Label(self.baseframe,text="Username",font=("Helvetica", 20)).grid(row=2,pady=10)
        Label(self.baseframe,text="Password",font=("Helvetica", 20)).grid(row=3,pady=10)

        self.username = Entry(self.baseframe,font=("Helvetica", 20))
        self.username.grid(row=2,column=2)
        self.password = Entry(self.baseframe, show="*",font=("Helvetica", 20))
        self.password.grid(row=3,column=2)

        self.submitBtn = Button(self.baseframe,text="Login",font=("Helvetica", 20),command=self.onSubmitPressed)
        self.submitBtn.grid(row=6,columnspan=3,rowspan=2,pady=10)


    def onSubmitPressed(self):
        if len(self.username.get()) == 0:
            messagebox.showerror("Incorrect Username", "Username can not be empty")
            return 
        if len(self.password.get())== 0:
            messagebox.showerror("Incorrect Password", "Password can not be empty")
            return 

        userdetails = auth_user(self.username.get(),self.password.get())

        if userdetails is None:
            messagebox.showerror("Login failed", "Username and password combination doesnot exits")
        else:
            print(userdetails[1])
            if userdetails[1]['privilege'] == 'admin':
                self.destroy()
                from adminDasboard import AdminDashboard
                adminscreen = AdminDashboard(userdetails = userdetails[1])
                adminscreen.mainloop()
            # adminDasboard.start(userdetails[1])
        



    def start(self):
        self.mainloop()

