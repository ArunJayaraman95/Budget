# Imports
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from tkinter import ttk
import csv
from tkcalendar import *
from random import randint
# Define colors
mainColor = "#70A0A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 24)
inputFont = ("Verdana", 20)
usernameFont = ("Verdana", 16)
aFont = ("Times New Roman", 20)
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
viewFrame.place(height = 500, width = 1000, relx = 0.5, rely = 0.6, anchor = CENTER)
viewFrame.config(highlightbackground='black', highlightthickness=4)

# Scrollbar and table setup
tableScroll = ttk.Scrollbar(viewFrame, orient = 'vertical')
tableScroll.pack(side = RIGHT, fill = Y)
testTree = ttk.Treeview(viewFrame, yscrollcommand= tableScroll.set)
tableScroll.config(command = testTree.yview)

# Define columns
testTree['columns'] = ("Date", "Name", "Planned", "Actual", "Difference", "Notes")

# Format columns
testTree.column("#0", width = 0, stretch = NO)
testTree.column("Date", width = 80, anchor = W)
testTree.column("Name", width = 120, anchor = W)
testTree.column("Planned", width = 150, anchor = E)
testTree.column("Actual", width = 150, anchor = E)
testTree.column("Difference", width = 150, anchor = E)
testTree.column("Notes", width = 330, anchor = E)



#testTree.heading("#0", text = "Label", anchor = W)
testTree.heading("Date", text = "Date", anchor = CENTER)
testTree.heading("Name", text = "Name", anchor = CENTER)
testTree.heading("Planned", text = "Planned", anchor = CENTER)
testTree.heading("Actual", text = "Actual", anchor = CENTER)
testTree.heading("Difference", text = "Difference", anchor = CENTER)
testTree.heading("Notes", text = "Notes", anchor = CENTER)


#testTree.insert(parent = '', index = 'end', iid = 0, text = "Parent", values = ("6/12", "Food", 300, 500))

#Add data
counter = 0
with open('UserData/'+activeUser+'.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            print(line)
            diff = round(float(line[3]) - float(line[2]), 3)
            diff = '-${:,.2f}'.format(-diff) if diff < 0 else '${:,.2f}'.format(diff) 
            exp = '${:,.2f}'.format(float(line[2])) 
            act = '${:,.2f}'.format(float(line[3])) 
            tempTuple = (line[0], line[1], exp, act, diff, "")
            testTree.insert(parent = '', index = 'end', iid = counter, text = "Parent", values = tempTuple)
            counter += 1

for i in range(40):
    testTree.insert(parent = '', index = 'end', iid = counter, text = "Parent", values = ("d", "n", randint(0, 100), randint(0, 100), 4, ""))
    counter += 1

# Pack table
testTree.pack()




# Formatting (font changes)
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 12))
style.configure("Treeview", font = ("Verdana", 16), rowheight = 50)

cal = Calendar(tableFrame, selectmode = "day", year = 2021, month = 6, day = 20, date_pattern = 'mm/dd/yy')
#cal.grid(row = 0, column = 0, pady = 20, padx = 20)
cal.pack(pady = 20)
calToggle = True
def toggleCalendar():
    global calToggle
    if calToggle:
        cal.pack_forget()
        calToggle = False
    else:
        cal.pack()
        calToggle = True

tb = Button(tableFrame, text = "Get date", command = toggleCalendar)
tb.pack(pady = 20, ipadx = 20, ipady = 20)



#endregion


root.mainloop()