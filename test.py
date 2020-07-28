from tkinter import *
from tkinter import messagebox,ttk
from PIL import Image,ImageTk
from db import addScreentoDb
import numpy as np



class AddScreenButton(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)

        self.valueVar = StringVar()
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
        self.RCount = IntVar()
        self.GCount = IntVar()
        self.PCount = IntVar()

        self.RCount.set(0)
        self.PCount.set(0)
        self.GCount.set(0)

        self.RPrice = IntVar()
        self.GPrice = IntVar()
        self.PPrice = IntVar()
        
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
        print(strLayout)
        print(type(strLayout))

        data = {"total_capcity" : self.RCount.get() + self.PCount.get() + self.GCount.get(),
        "regular_seats": self.RCount.get(),
        "regular_price":self.RPrice.get(),
        "preminum_seats":self.PCount.get(),
        "preminum_prices":self.PPrice.get(),
        "gold_seats":self.GCount.get(),
        "gold_price":self.GPrice.get(),
        "layout":strLayout}

        addScreentoDb(data)




    def start(self):
        self.mainloop()



AddScreen().mainloop()