from tkinter import *
from tkinter import messagebox,ttk
from PIL import Image,ImageTk
import requests
import numpy as np
from api import searchMovie,getMovieDetails
from io import BytesIO
import db
from db import addScreentoDb,getAllMovie,getAllScreens

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
        self.listOfMovies  = getAllMovie()  
        self.listOfMoviesNames  = []

        for row in self.listOfMovies:
            self.listOfMoviesNames.append(row[1])

        if self.listOfMovies == None:
            messagebox.showerror('Error',"No Moive Exits ,Please add movie before adding projection")
            self.destroy()  
        else:
            self.onCreate()

    def onCreate(self):
        HEIGHT = 800
        WIDTH  = 450
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)

        Label(frame,text="Add New Projection",font=("Helvetica", 12)).grid(row=0,columnspan=2,pady=15,padx=15)

        Label(frame,text="Select Movie: ").grid(row=1,pady=10)
        Label(frame,text="Select Auditorium/Screen: ").grid(row=2,pady=10)
        Label(frame,text="Select Start Date Time: ").grid(row=3,pady=10)
        Label(frame,text="Select End Date Time: ").grid(row=4,pady=10)

        moviesChkbox = ttk.Combobox(master=frame)
        moviesChkbox['values'] = self.listOfMoviesNames
        moviesChkbox.grid(row=1,column=1,pady=10)

        print(moviesChkbox.current())
       
       
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


class AddScreenButton(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)

        self.valueVar = StringVar(master=self)
        self.valueVar.set(" ")
        self.config(textvariable=self.valueVar)
        self.bind("<ButtonPress>", self.on_press)


    def on_press(self, event):
        var = self.valueVar.get()

        
        if var == " ":
            self.valueVar.set("R")
        
        elif var == "R":
            self.valueVar.set("P")
                    
        elif var == "P":
            self.valueVar.set("G")
        
        elif var  == "G":
            self.valueVar.set(" ")
       
        print("Button Pressed: ",self.valueVar.get())

    def getValue(self):
        return self.valueVar.get()

    def setValue(self,Value):
        return self.valueVar.set(Value)
        
        
       
class  AddScreen(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.layout = [[0 for _ in range(20)] for _ in range(15)]
        self.isLayout =False
        self.RCount = IntVar(master=self)
        self.GCount = IntVar(master=self)
        self.PCount = IntVar(master=self)

        self.RCount.set(0)
        self.PCount.set(0)
        self.GCount.set(0)

        self.RPrice = IntVar(master=self)
        self.GPrice = IntVar(master=self)
        self.PPrice = IntVar(master=self)
        
        self.RPrice.set(80)
        self.PPrice.set(120)
        self.GPrice.set(150)

        self.onCreate()

    def onCreate(self):
        
        
        HEIGHT = 800
        WIDTH  = 800
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        Label(frame,text="Add New Screen ",font=("Helvetica", 12)).pack()
        
        headerFrame = Frame(frame)
        headerFrame.pack(pady=10,padx=10)

        Label(headerFrame,text="Please set auditorium layout and set ticket Prices For Each Category").grid(row=0,columnspan=4)    
        Label(headerFrame,text="No Of Regular Sets: ").grid(row=1,column=0)    
        Label(headerFrame,text="No Of Premium Sets: ").grid(row=2,column=0)    
        Label(headerFrame,text="No Of Gold Sets: ").grid(row=3,column=0)

        self.noOfRegularSeats = Entry(headerFrame,textvariable=self.RCount)    
        self.noOfPremiumSeats = Entry(headerFrame,textvariable=self.PCount)    
        self.noOfGoldSeats = Entry(headerFrame,textvariable=self.GCount)    
        
        self.noOfRegularSeats.grid(row=1 ,column=1)
        self.noOfPremiumSeats.grid(row=2 ,column=1)
        self.noOfGoldSeats.grid(row=3 ,column=1)

        Label(headerFrame,text="Price Of Regular Sets: ₹").grid(row=1,column=2)    
        Label(headerFrame,text="Price Of Premium Sets: ₹").grid(row=2,column=2)    
        Label(headerFrame,text="Price Of Gold Sets: ₹").grid(row=3,column=2)

        self.priceOfRegularSeats = Entry(headerFrame,textvariable=self.RPrice)    
        self.priceOfPremiumSeats = Entry(headerFrame,textvariable=self.PPrice)    
        self.priceOfGoldSeats = Entry(headerFrame,textvariable=self.GPrice)    
        
        self.priceOfRegularSeats.grid(row=1 ,column=3)
        self.priceOfPremiumSeats.grid(row=2 ,column=3)
        self.priceOfGoldSeats.grid(row=3 ,column=3)

        Label(headerFrame,text="R = Regular Seat , P = Premium Seat , G = Gold Seat , 'BLANK' = No Seat ").grid(row=4,columnspan=4,pady=10,padx=10)    



        layoutFrame = Frame(frame,bg="grey")
        layoutFrame.pack(pady=15,padx=15)

        self.ListOfSeats = []
        for i in range(len(self.layout)):
            for j in range(len(self.layout[0])):
                btn = AddScreenButton(master=layoutFrame,width=2)
                btn.config(
                    command = lambda btn=btn:self.seatPressed(btn=btn))
                if i < 8:
                    btn.setValue("R")

                    self.RCount.set(self.RCount.get()+1)
                elif  i < 13:
                    btn.setValue("P")
                    self.PCount.set(self.PCount.get()+1)

                elif  i <15:
                    btn.setValue("G")
                    self.GCount.set(self.GCount.get()+1)


               
                btn.grid(row=i,column=j,pady=2,padx=2)
                self.ListOfSeats.append(btn)


        SetBtn = Button(frame,text = "Set Layout",command=self.setLayout)
        SetBtn.pack()
    
    def seatPressed(self,btn):
        var = btn.getValue()
        if var == " ":
            self.GCount.set(self.GCount.get() - 1)
        
        elif var == "R":
            self.RCount.set(self.RCount.get() + 1)   

        elif var == "P":
            self.RCount.set(self.RCount.get() - 1)   
            self.PCount.set(self.PCount.get() + 1)   

        
        elif var  == "G":
            self.PCount.set(self.PCount.get() - 1)   
            self.GCount.set(self.GCount.get() + 1)


        

    def setLayout(self):
        
        matrix = [btn.getValue() for btn in self.ListOfSeats ]
        z = 0
        for i in range(0,15):
            for j in range(0,20):
                self.layout[i][j] = matrix[z]
                z += 1

        self.isLayout = True

        for row in self.layout:
            # print(row)
            pass

        npLayout = np.array(self.layout)
        strLayout = npLayout.tostring()

        data = {"total_capcity" : self.RCount.get() + self.PCount.get() + self.GCount.get(),
        "regular_seats": self.RCount.get(),
        "regular_price":self.RPrice.get(),
        "preminum_seats":self.PCount.get(),
        "preminum_prices":self.PPrice.get(),
        "gold_seats":self.GCount.get(),
        "gold_price":self.GPrice.get(),
        "layout":strLayout}

        msg = addScreentoDb(data)
        if msg[0] == 0:
            messagebox.showinfo("Success", msg[1])
    
        if msg[0] == 1:
            messagebox.showerror("Error", msg[1])






    def start(self):
        self.mainloop()

class  EditScreen(Tk):
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
        Label(frame,text="Edit Screen ",font=("Helvetica", 12)).pack()

    def start(self):
        self.mainloop()


class  ManageScreen(Tk):
    def __init__(self,userdetails={}):
        Tk.__init__(self)
        self.userdetails = userdetails
        
        self.onCreate()

    def onCreate(self):
        
        
        HEIGHT = 800
        WIDTH  = 800
        canvas = Canvas(self, height=HEIGHT,width=WIDTH)
        canvas.pack()
        frame = Frame(canvas,bg="grey")
        frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)
        Label(frame,text="Manage Screens/Auditoruim",font=("Helvetica", 12)).grid(row=0,columnspan=3,pady=10,padx=10,)

        addBtn = Button(frame ,text="Add New Auditorium",command=self.addScreen)
        addBtn.grid(row=1,column=0,padx=10,pady=10,sticky='nesw')

        removeBtn = Button(frame ,text="Remove Auditouriom")
        removeBtn.grid(row=1,column=1,padx=10,pady=10,sticky='nesw')

        editBtn = Button(frame ,text="Edit Existing Auditurioum",command=self.editScreen)
        editBtn.grid(row=1,column=2,padx=10,pady=10,sticky='nesw')

        self.lb = Listbox(frame)
        self.lb.grid(row=2,columnspan=3)


    def addScreen(self):
        self.destroy()
        AddScreen().start()
    
    def editScreen(self):
        self.destroy()
        EditScreen().start()

    def populate(self):
        pass

    def start(self):
        self.mainloop()


    def destory(self):
        self.destroy()


