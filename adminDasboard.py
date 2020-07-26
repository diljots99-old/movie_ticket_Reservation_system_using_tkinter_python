from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db import auth_user

from api import *
from tkObjects import *
from tkinter.filedialog import askopenfilename


class  AdminDashboard(Tk):
    def __init__(self,userdetails={}):
        Tk.__init__(self)
        self.userdetails = userdetails
        self.onCreate()
      


    def onCreate(self):
        # Top Level Start

        HEIGHT = 900
        WIDTH  = 1600
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        # Top Level End


        # Top Menu Bar Code Start

        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.NewFile)
        self.filemenu.add_command(label="Open...", command=self.OpenFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Logout", command=self.Logout)
        self.filemenu.add_command(label="Exit", command=self.quit)

        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.About)
        # Top Menu Bar Code END


        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        greeting = Label(frame,text=f"Welcome {self.userdetails['username']}, Admin DashBoard",font=("Helvetica", 35))
        greeting.pack(pady=5)

        # Right Side Button Start
        add_new_employee = Button(frame,text="Add new Employee",command=self.addNewEmployee)
        add_new_movie = Button(frame,text="Add New Movie",command=self.addNewMovie)
        add_new_projection = Button(frame,text="Add New Projection",command=self.addNewProjection)
        search_movie =  Button(frame,text="Search Movies",command=self.searchMovie)
        manage_screens =  Button(frame,text="Manage Screen/Auditoriums",command=self.manageScreen)

        
        add_new_employee.place(relx=0.80,rely=0.10,relwidth=0.15)
        add_new_movie.place(relx=0.80,rely=0.20,relwidth=0.15)
        add_new_projection.place(relx=0.80,rely=0.30,relwidth=0.15)
        search_movie.place(relx=0.80,rely=0.40,relwidth=0.15)
        manage_screens.place(relx=0.80,rely=0.50,relwidth=0.15)
        # Right Side Button End

        # Header
        

        header_frame = Canvas(frame)
        header_frame.place(relx=0.01,rely=0.10,relwidth=0.75,relheight=.30)

        scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=header_frame.xview)
        scrollable_frame = ttk.Frame(header_frame)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: header_frame.configure(
                scrollregion=header_frame.bbox("all")
            )
        )

        upcoming_movie = get_upcoming_movies(region='in')
        header_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")
        header_frame.configure(yscrollcommand=scrollbar.set)

        scrollbar.place(relx=0.01,rely=0.40,relwidth=0.75)

        Label(scrollable_frame,text="Upcoming Movies",font=("Helvetica", 20)).grid(row=0,columnspan=5,stick=W)
       
      
        i = 0
        if upcoming_movie:
            for movie in upcoming_movie:
                print(movie['title'])
                frmae = DisplayPoster(master=scrollable_frame,movie=movie,height=160,width=90)
                frmae.grid(row= 1,column=i,pady=10,padx=10)
                i += 1

    def start(self):
        self.mainloop()


    def destory(self):
        self.destroy()


    # Top Menu Bar Comands start

    def NewFile(self):
        print("New File!")
    def OpenFile(self):
        name = askopenfilename()
        print(name)
    def About(self):
        print("This is a simple example of a menu")
    def Logout(self):
        self.destroy()
        from login import start
        start()
    # Top Menu Bar Comands End

    def addNewMovie(self):
        AddNewMovie(self.userdetails) .start()


    def addNewEmployee(self):
        AddNewMovie(self.userdetails) .start()

    def addNewProjection(self):
        AddNewProjection(self.userdetails) .start()

    def searchMovie(self):
        SearchMovie(self.userdetails) .start()

    def manageScreen(self):
        ManageScreen(self.userdetails) .start()












