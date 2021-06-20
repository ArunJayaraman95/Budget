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


tableFrame = Frame(root, background = mainColor)
tableFrame.grid(row = 0, column = 0, sticky = "nsew")

showFrame(tableFrame)


#region Frame1
#============Frame 1 ==============# 
# Variables
activeUser = "test"

# Create subframe
viewFrame = Frame(tableFrame, bg = accentColor)

# Labels
testTree = ttk.Treeview(tableFrame)

# Define columns
testTree['columns'] = ("Date", "Name", "Planned", "Actual", "Difference")

# Format columns
testTree.column("#0", width = 0, stretch = NO)
testTree.column("Date", anchor = W)
testTree.column("Name", anchor = W)
testTree.column("Planned", anchor = E)
testTree.column("Actual", anchor = E)
testTree.column("Difference", anchor = E)


#testTree.heading("#0", text = "Label", anchor = W)
testTree.heading("Date", text = "Date", anchor = CENTER)
testTree.heading("Name", text = "Name", anchor = CENTER)
testTree.heading("Planned", text = "Planned", anchor = CENTER)
testTree.heading("Actual", text = "Actual", anchor = CENTER)
testTree.heading("Difference", text = "Difference", anchor = CENTER)
#Add data
#testTree.insert(parent = '', index = 'end', iid = 0, text = "Parent", values = ("6/12", "Food", 300, 500))

counter = 0
with open('UserData/'+activeUser+'.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            print(line)
            diff = float(line[3]) - float(line[2])
            diff = str('-$' + str(-diff)) if diff < 0 else '$' + str(diff) 
            tempTuple = (line[0], line[1], '$' + line[2], '$' + line[3], diff)
            testTree.insert(parent = '', index = 'end', iid = counter, text = "Parent", values = tempTuple)
            counter += 1

for i in range(40):
    testTree.insert(parent = '', index = 'end', iid = counter, text = "Parent", values = tempTuple)
    counter += 1
testTree.pack(pady = 20)
vsb = ttk.Scrollbar(tableFrame, orient = 'vertical', command = testTree.yview)
vsb.pack(side = 'right', fill = 'y')
#endregion


root.mainloop()