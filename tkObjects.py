from tkinter import *
from tkinter import messagebox,ttk
from PIL import Image,ImageTk
import requests

from api import searchMovie,getMovieDetails
from io import BytesIO
import db

class DisplayPoster(Frame):
    def __init__(self,movie=None,height=160,width=90, *args, **kwargs):
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
            print(poster_path)
            # url = f'http://image.tmdb.org/t/p/original/{poster_path}'
            url = f'http://image.tmdb.org/t/p/w500/{poster_path}'
            r = requests.get(url, allow_redirects=True)

            if r.status_code == 200:
                image = Image.open(BytesIO(r.content)).resize((width,height), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image,master=self)
                return img
            else:
                image = Image.open("poster_placeholder_light.png").resize((width,height), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image,master=self)  
                return img
        except :
            image = Image.open("poster_placeholder_light.png").resize((width,height), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image,master=self)  
            return img

class  SearchResult(Tk):
    def __init__(self,listOfMovies=None):
        Tk.__init__(self,)
        self.listOfMoives = listOfMovies
        self.onCreate()

    def onCreate(self):
        
        
        HEIGHT = 800
        WIDTH  = 800
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        Label(frame,text="Search Results",font=("Helvetica", 12)).pack()

        header_frame = Canvas(frame)
        header_frame.place(relx=0.01,rely=0.10,relwidth=0.95,relheight=.30)

        scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=header_frame.xview)
        scrollable_frame = ttk.Frame(header_frame)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: header_frame.configure(
                scrollregion=header_frame.bbox("all")
            )
        )

        header_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")
        header_frame.configure(yscrollcommand=scrollbar.set)

        scrollbar.place(relx=0.01,rely=0.40,relwidth=0.95)

              
        i = 0
        for movie in self.listOfMoives:
            print(movie['title'])
            frmae = DisplayPoster(master=scrollable_frame,movie=movie,height=160,width=90)
            frmae.grid(row= 1,column=i,pady=10,padx=10)
            btn = Button(master=scrollable_frame,text=movie['title'],command=lambda  movie=movie : self.onResultClicked(Movie=movie))
            btn.grid(row= 2,column=i,padx=10)
            i += 1

        self.movieFrame = Frame(frame)
        self.movieFrame.place(relx=0.01,rely=0.45,relwidth=0.95,relheight=.45)

        

        
      
    def onResultClicked(self,Movie=None):

        for child in self.movieFrame.winfo_children():
            child.destroy()

        movie = getMovieDetails(Movie['id'])
        self.selectedMovie = movie
        if movie is not None:
            Label(self.movieFrame,text= "Movie Details",font=("Helvetica", 15)).grid(row=0,columnspan=4)

            Label(self.movieFrame,text="Title",font=("Helvetica", 12)).grid(row=2,column=0,padx=10,pady=10)
            Label(self.movieFrame,text= movie['title'],font=("Helvetica", 12)).grid(row=2,column=1,padx=10,pady=10)

            Label(self.movieFrame,text="Adult",font=("Helvetica", 12)).grid(row=2,column=2,padx=10,pady=10)
            Label(self.movieFrame,text= movie["adult"],font=("Helvetica", 12)).grid(row=2,column=3,padx=10,pady=10)
            
            Label(self.movieFrame,text="Status",font=("Helvetica", 12)).grid(row=3,column=0,padx=10,pady=10)
            Label(self.movieFrame,text=movie["status"],font=("Helvetica", 12)).grid(row=3,column=1,padx=10,pady=10)

            Label(self.movieFrame,text="Release Date",font=("Helvetica", 12)).grid(row=3,column=2,padx=10,pady=10)
            Label(self.movieFrame,text=movie["release_date"],font=("Helvetica", 12)).grid(row=3,column=3,padx=10,pady=10)

            Label(self.movieFrame,text="Tagline",font=("Helvetica", 12)).grid(row=4,column=0,padx=10,pady=10)
            Label(self.movieFrame,text=movie["tagline"],wraplength=500,font=("Helvetica", 12)).grid(row=4,column=1,columnspan=3,padx=10,pady=10)

            Label(self.movieFrame,text="Overview",font=("Helvetica", 12)).grid(row=5,column=0,padx=10,pady=10)
            Label(self.movieFrame,text=movie["overview"],wraplength=500,font=("Helvetica", 12)).grid(row=5,column=1,columnspa=3,padx=10,pady=10)
        

            addBtn = Button(self.movieFrame,text="Add Movie to System",font=("Helvetica", 12),command=self.addToDb)
            addBtn.grid(row=6,column=0,columnspa=2,padx=10,pady=15)

            clearBtn = Button(self.movieFrame,text="Clear",font=("Helvetica", 12),command = lambda  frame=self.movieFrame : self.clearFrame(frame=frame))
            clearBtn.grid(row=6,column=2,columnspa=2,padx=10,pady=15)
    
            exitBtn = Button(self.movieFrame,text="Exit",font=("Helvetica", 12),command = self.destroy)
            exitBtn.grid(row=6,column=4,columnspa=2,padx=10,pady=15)
    
             

    def addToDb(self):
        msg = db.addMoie(movie=self.selectedMovie)
        if msg[0] == 0:
            messagebox.showinfo("Success", msg[1])
    
        if msg[0] == 1:
            messagebox.showerror("Error", msg[1])

        print( self.selectedMovie['title'])

    def clearFrame(self,frame):
        self.selectedMovie = None
        for child in self.movieFrame.winfo_children():
            child.destroy()
        
    def start(self):
        self.mainloop()


    def destory(self):
        self.destroy()



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
        self.frame = Frame(canvas,bg="grey")
        self.frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        Label(self.frame,text="Add New Movie",font=("Helvetica", 25)).grid(row=0,columnspan=2,padx=10,pady=10)


        self.searchMovie_entry = Entry(self.frame)
        self.searchMovie_entry.grid(row=1,padx=10,pady=10)

        self.searchMovie_btn = Button(self.frame,text="Search",command=self.searchMovie_tmdb)
        self.searchMovie_btn.grid(row=1,column=1,padx=10,pady=10)


        Label(self.frame,text="Title",font=("Helvetica", 12)).grid(row=2,column=0,padx=10,pady=10)
        Label(self.frame,text="Tagline",font=("Helvetica", 12)).grid(row=3,column=0,padx=10,pady=10)
        Label(self.frame,text="Adult",font=("Helvetica", 12)).grid(row=4,column=0,padx=10,pady=10)
        Label(self.frame,text="Status",font=("Helvetica", 12)).grid(row=5,column=0,padx=10,pady=10)
        Label(self.frame,text="Overview",font=("Helvetica", 12)).grid(row=6,column=0,padx=10,pady=10)
        Label(self.frame,text="Backdrop",font=("Helvetica", 12)).grid(row=7,column=0,padx=10,pady=10)
        Label(self.frame,text="Poster",font=("Helvetica", 12)).grid(row=8,column=0,padx=10,pady=10)
        Label(self.frame,text="Release Date",font=("Helvetica", 12)).grid(row=9,column=0,padx=10,pady=10)


        self.title_entry = Entry(self.frame)
        self.tagline_entry = Entry(self.frame)
        self.adult_entry = Entry(self.frame)
        self.status_entry = Entry(self.frame)
        self.overview_entry = Entry(self.frame)
        self.release_date_entry = Entry(self.frame)
        self.poster_entry = Entry(self.frame)
        self.backdrop_entry = Entry(self.frame)

        
        self.title_entry.grid(row=2,column=1,padx=10,pady=10)
        self.tagline_entry.grid(row=3,column=1,padx=10,pady=10)
        self.adult_entry.grid(row=4,column=1,padx=10,pady=10)
        self.status_entry.grid(row=5,column=1,padx=10,pady=10)
        self.overview_entry.grid(row=6,column=1,padx=10,pady=10)
        self.backdrop_entry.grid(row=7,column=1,padx=10,pady=10)
        self.poster_entry.grid(row=8,column=1,padx=10,pady=10)
        self.release_date_entry.grid(row=9,column=1,padx=10,pady=10)


    def searchMovie_tmdb(self):
        searchQuery = str(self.searchMovie_entry.get())
        if searchQuery == "" or searchQuery == None:
            messagebox.showerror("No Search query", "Search Query is needed to search")
        else:
            
            res = searchMovie(searchQuery)
            if res is not None:
                self.destroy()
                SearchResult(listOfMovies=res).start()
                
            else:
                messagebox.showerror("No Search Result", "No results Found Try Manual Entry")


            print(searchQuery)
            print(res)



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


