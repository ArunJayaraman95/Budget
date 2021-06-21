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


budgetFrame = Frame(root, background = mainColor)
budgetFrame.grid(row = 0, column = 0, sticky = "nsew")

showFrame(budgetFrame)


#region Frame1
#============Frame 1 ==============# 
# Variables
activeUser = "test"

tableFrame = Frame(budgetFrame, background = accentColor)
tableFrame.place(height = 700, width = 1000, relx = 0.5, rely = 0.5, anchor = CENTER)
# Create subframe
viewFrame = Frame(tableFrame, bg = accentColor)
#viewFrame.place(height = 500, width = 1000, relx = 0.5, rely = 0.05, anchor = N)
viewFrame.grid(row = 0, column = 0, columnspan = 5)
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
expenseCount = 0
with open('UserData/'+activeUser+'.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            print(line)
            diff = round(float(line[3]) - float(line[2]), 3)
            diff = '-${:,.2f}'.format(-diff) if diff < 0 else '${:,.2f}'.format(diff) 
            exp = '${:,.2f}'.format(float(line[2])) 
            act = '${:,.2f}'.format(float(line[3])) 
            tempTuple = (line[0], line[1], exp, act, diff, "")
            testTree.insert(parent = '', index = 'end', iid = expenseCount, text = "Parent", values = tempTuple)
            expenseCount += 1

for i in range(40):
    testTree.insert(parent = '', index = 'end', iid = expenseCount, text = "Parent", values = ("d", "n", randint(0, 100), randint(0, 100), 4, ""))
    expenseCount += 1

# Pack table
testTree.pack()

# Table editor

dl = Label(tableFrame, text = "Date")
nl = Label(tableFrame, text = "Name")
pl = Label(tableFrame, text = "Planned")
al = Label(tableFrame, text = "Actual")
ml = Label(tableFrame, text = "Notes")

columnList = [dl, nl, pl, al, ml]

for i, col in enumerate(columnList):
    col.grid(row = 1, column = i, pady = 20)
    col.config(bg = accentColor)

# Entry boxes to edit
de = Entry(tableFrame)
ne = Entry(tableFrame)
pe = Entry(tableFrame)
ae = Entry(tableFrame)
me = Entry(tableFrame)

editList = [de, ne, pe, ae, me]
for i, ent in enumerate(editList):
    ent.grid(row = 2, column = i)

# Button functions
def addExpense():
    global expenseCount
    testTree.insert(parent = '', index = 'end', iid = expenseCount, text = "Parent",values = (de.get(), ne.get(), pe.get(), ae.get(), float(pe.get()) - float(ae.get()), me.get()))
    expenseCount += 1
    # Delete entries
    for col in editList:
        col.delete(0, END)

def removeAll():
    for record in testTree.get_children():
        testTree.delete(record)
# Buttons
addButton = Button(tableFrame, text = "Add expense", command = addExpense)
addButton.grid(row = 3, column = 0, pady = 20)

delButton = Button(tableFrame, text = "Remove all expenses", command = removeAll)
delButton.grid(row = 3, column = 1, pady = 20)

# Formatting (font changes)
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 12))
style.configure("Treeview", font = ("Verdana", 16), rowheight = 50)

















# Calendar
cal = Calendar(budgetFrame, selectmode = "day", year = 2021, month = 6, day = 20, date_pattern = 'mm/dd/yy')
#cal.grid(row = 0, column = 0, pady = 20, padx = 20)
#cal.pack(pady = 20)
calToggle = True

def toggleCalendar():
    global calToggle
    if calToggle:
        cal.pack_forget()
        calToggle = False
    else:
        cal.pack()
        calToggle = True

# Toggle Calendar button
#tb = Button(budgetFrame, text = "Get date", command = toggleCalendar)
#tb.pack(pady = 20, ipadx = 20, ipady = 20)

#


#endregion


root.mainloop()