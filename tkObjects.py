from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import requests
from io import BytesIO

class DisplayPoster(Frame):
    def __init__(self,movie={},height=160,width=90, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.movie = movie
        self.height = height
        self.width = width
        self.imageHeight = height
        self.imageWidth = width
        self.onCreate()
        


    def onCreate(self):
        img = self.get_poster_image(self.imageHeight,self.imageWidth)
        posterImage = Label(self,image=img)
        posterImage.image=img
        posterImage.pack()
        
        movieTitle = self.movie['title']
        posterLabel = Label(self,text=movieTitle,font=("Helvetica", 12))
        posterLabel.pack()

   
    def get_poster_image(self,height,width):
        try:
            poster_path = self.movie['poster_path']

            # url = f'http://image.tmdb.org/t/p/original/{poster_path}'
            url = f'http://image.tmdb.org/t/p/w500/{poster_path}'
            r = requests.get(url, allow_redirects=True)

            if r.status_code == 200:
                image = Image.open(BytesIO(r.content)).resize((width,height), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image)
                return img
            else:
                image = Image.open("poster_placeholder_light.png").resize((width,height), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image)  
                return img
        except :
            image = Image.open("poster_placeholder_light.png").resize((width,height), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)  
            return img

class  AddNewMovie(Tk):
    def __init__(self,userdetails={}):
        Tk.__init__(self)
        self.userdetails = userdetails
        self.onCreate()

    def onCreate(self):
        
        
        HEIGHT = 800
        WIDTH  = 450
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        Label(frame,text="Add New Movie",font=("Helvetica", 12)).pack()


    def start(self):
        self.mainloop()


    def destory(self):
        self.destroy()

class  AddNewEmployee(Tk):
    def __init__(self,userdetails={}):
        Tk.__init__(self)
        self.userdetails = userdetails
        self.onCreate()

    def onCreate(self):
        
        
        HEIGHT = 800
        WIDTH  = 450
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        Label(frame,text="Add New Empolyee",font=("Helvetica", 12)).pack()

    def start(self):
        self.mainloop()


    def destory(self):
        self.destroy()

class  AddNewProjection(Tk):
    def __init__(self,userdetails={}):
        Tk.__init__(self)
        self.userdetails = userdetails
        self.onCreate()

    def onCreate(self):
        
        
        HEIGHT = 800
        WIDTH  = 450
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        Label(frame,text="Add New Projection",font=("Helvetica", 12)).pack()


    def start(self):
        self.mainloop()


    def destory(self):
        self.destroy()

class  SearchMovie(Tk):
    def __init__(self,userdetails={}):
        Tk.__init__(self)
        self.userdetails = userdetails
        self.onCreate()

    def onCreate(self):
        
        
        HEIGHT = 800
        WIDTH  = 450
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        Label(frame,text="Search Movie",font=("Helvetica", 12)).pack()

    def start(self):
        self.mainloop()


    def destory(self):
        self.destroy()

class  ManageScreen(Tk):
    def __init__(self,userdetails={}):
        Tk.__init__(self)
        self.userdetails = userdetails
        self.onCreate()

    def onCreate(self):
        
        
        HEIGHT = 800
        WIDTH  = 450
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        Label(frame,text="Manage Screens/Auditoruim",font=("Helvetica", 12)).pack()

    def start(self):
        self.mainloop()


    def destory(self):
        self.destroy()