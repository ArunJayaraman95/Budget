# Imports
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from tkinter import ttk
import csv

# Define colors
mainColor = "#70A0A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 24)
inputFont = ("Verdana", 20)
usernameFont = ("Verdana", 16)

def showFrame(frame):
    frame.tkraise()

# Creating window
root=Tk()
root.state("zoomed")  #Makes it fullscreen automatically
sx = root.winfo_screenwidth() 
sy = root.winfo_screenheight()

# Set the window size
root.geometry("%dx%d" % (sx, sy))
root.title("Budget Boi")
root.iconbitmap("img/WayneStateLogo.ico")

# Configurations
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)


tableFrame = Frame(root, background = 'red')
tableFrame.grid(row = 0, column = 0, sticky = "nsew")

showFrame(tableFrame)


#region Frame1
#============Frame 1 ==============# 
# Variables
activeUser = "test"

# Create subframe
viewFrame = Frame(tableFrame, bg = 'red')

# Labels
testTree = ttk.Treeview(tableFrame)

# Define columns
testTree['columns'] = ("Date", "Name", "Planned", "Actual")

# Format columns
testTree.column("#0", width = 120, minwidth = 25)
testTree.column("Date", anchor = W)
testTree.column("Name", anchor = W)
testTree.column("Planned", anchor = E)
testTree.column("Actual", anchor = E)

testTree.heading("#0", text = "Label", anchor = W)
testTree.heading("Date", text = "Date", anchor = W)
testTree.heading("Name", text = "Name", anchor = W)
testTree.heading("Planned", text = "Planned", anchor = CENTER)
testTree.heading("Actual", text = "Actual", anchor = CENTER)

#Add data
testTree.insert(parent = '', index = 'end', iid = 0, text = "Parent", values = ("6/12", "Food", 300, 500))

testTree.pack(pady = 20)




#endregion


root.mainloop()