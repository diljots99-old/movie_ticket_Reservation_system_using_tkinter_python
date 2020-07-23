from tkinter import *
from tkinter import messagebox
from db import auth_user

from tkinter.filedialog import askopenfilename


# Top Menu Bar Comands start

def NewFile():
    print("New File!")
def OpenFile():
    name = askopenfilename()
    print(name)
def About():
    print("This is a simple example of a menu")
def Logout():
    dismiss_window()

    from login import start
    start()
# Top Menu Bar Comands End



# Top Level Start
window =Tk()
HEIGHT = 900
WIDTH  = 1600
canvas = Canvas(window, height=HEIGHT,width=WIDTH)
canvas.pack()
# Top Level End


# Top Menu Bar Code Start

menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Logout", command=Logout)
filemenu.add_command(label="Exit", command=window.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)
# Top Menu Bar Code END




frame = Frame(canvas,bg="grey")
frame.place(relx=0.01,rely=0.01,relwidth=0.98, relheight=0.98)


add_new_theater = Button(frame,text="add new theater")
add_new_employee = Button(frame,text="add new Employee")
add_new_movie = Button(frame,text="Add New Movie")

add_new_theater.place(relx=0.80,rely=0.10)
add_new_employee.place(relx=0.80,rely=0.20)
add_new_movie.place(relx=0.80,rely=0.30)



def start(userdetails={}):
    print("admindashbord",userdetails)
    window.mainloop()

def dismiss_window():
    window.destroy()
start()