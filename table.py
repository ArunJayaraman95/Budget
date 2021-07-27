#region Imports and Config
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
from tkcalendar import *
import xlsxwriter as xw
import pyrebase
import urllib

# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyB07JiaeBfXONn4Sz4TvdJ4xWQqE3X21D8",
    "authDomain": "budget-software.firebaseapp.com",
    "databaseURL": "https://budget-software-default-rtdb.firebaseio.com/",
    "projectId": "budget-software",
    "storageBucket": "budget-software.appspot.com",
    "messagingSenderId": "124067844106",
    "appId": "1:124067844106:web:ccc1224030c1958a3a8ff3",
    "measurementId": "G-8MHJ83WY4T"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

# Define colors
mainColor = "#70A0A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 24)
inputFont = ("Verdana", 20)
usernameFont = ("Verdana", 16)
aFont = ("Times New Roman", 20)

# Function to display new page(frame)
def showFrame(frame):
    frame.tkraise()

# Creating window
root=Tk()
root.state("zoomed")  #Fullscreen
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
#endregion Window config

#region ========= Frame 1 ============# 

#region Frame configuration
# Variables
activeUser = "test"
income = 0

tableFrame = Frame(budgetFrame, background = accentColor)
tableFrame.place(height = 700, width = 1000, relx = 0.5, rely = 0.5, anchor = CENTER)
# Create subframe
viewFrame = Frame(tableFrame, bg = accentColor)
#viewFrame.place(height = 500, width = 1000, relx = 0.5, rely = 0.05, anchor = N)
viewFrame.grid(row = 0, column = 0, columnspan = 5)
viewFrame.config(highlightbackground='black', highlightthickness=0)

# Label to Display Month:
budget_date_label = Label(budgetFrame, text = "Viewing budget for 06/2021", bg = 'red')
budget_date_label.grid(row = 1, column = 0, pady = 10, padx = 10)

viewMonthEntry = Entry(budgetFrame)
viewMonthEntry.grid(row = 2, column = 0, pady = 10, padx = 10)

incomeLabel = Label(budgetFrame, text = "Income Stream", bg = 'yellow')
incomeLabel.grid(row = 4, column = 0, pady = 10, padx = 10)

incomeEntry = Entry(budgetFrame)
incomeEntry.grid(row = 5, column = 0, pady = 10, padx = 10)

def setIncome():
    income = incomeEntry.get()
    incomeLabel.config(text = "Income: " + str(income))
incomeButton = Button(budgetFrame, text = "View", command = setIncome)
incomeButton.grid(row = 6, column = 0, pady = 10, padx = 10)


# Set VIEWMONTH to this number
viewMonth = "06"

# Function to switch table based on viewMonthEntry
def updateTable():
    global viewMonth
    vm = viewMonthEntry.get()
    if int(vm) >= 1 and int(vm) <= 12:
        if len(vm) == 1:
            vm = '0' + vm
        viewMonth = vm
        displayCurrentMonth()
    else:
        messagebox.showwarning("Invalid Input!", "Month must be an integer from 1 to 12")

confirmViewMonth = Button(budgetFrame, text = "View", command = updateTable)
confirmViewMonth.grid(row = 3, column = 0, pady = 10, padx = 10)


# Scrollbar and table setup
tableScroll = ttk.Scrollbar(viewFrame, orient = 'vertical')
tableScroll.pack(side = RIGHT, fill = Y)
budgetTree = ttk.Treeview(viewFrame, yscrollcommand= tableScroll.set, selectmode = 'browse')
tableScroll.config(command = budgetTree.yview)
# Define columns
budgetTree['columns'] = ("Date", "Name", "Planned", "Actual", "Difference", "Notes")

# Format columns
budgetTree.column("#0", width = 0, stretch = NO)
budgetTree.column("Date", width = 140, anchor = W)
budgetTree.column("Name", width = 120, anchor = W)
budgetTree.column("Planned", width = 150, anchor = E)
budgetTree.column("Actual", width = 150, anchor = E)
budgetTree.column("Difference", width = 150, anchor = E)
budgetTree.column("Notes", width = 270, anchor = E)

#testTree.heading("#0", text = "Label", anchor = W)
budgetTree.heading("Date", text = "Date", anchor = CENTER)
budgetTree.heading("Name", text = "Name", anchor = CENTER)
budgetTree.heading("Planned", text = "Planned", anchor = CENTER)
budgetTree.heading("Actual", text = "Actual", anchor = CENTER)
budgetTree.heading("Difference", text = "Difference", anchor = CENTER)
budgetTree.heading("Notes", text = "Notes", anchor = CENTER)

budgetTree.tag_configure('oddrow', background = "white")
budgetTree.tag_configure('evenrow', background = "blue")

#endregion Frame Configuration

# Generate tuple from data for updates/insertions
# This removes dollar signs and commas from monatory values
def toTuple(date, name, planned, actual, notes = ""):
    a = date
    b = name
    c = '${:,.2f}'.format(float(planned)) 
    d = '${:,.2f}'.format(float(actual)) 
    e = round(float(planned) - float(actual), 2)
    e = '-${:,.2f}'.format(-e) if e < 0 else '${:,.2f}'.format(e)
    if notes:
        f = notes
    else:
        f = ""
    return (a, b, c, d, e, f)


def displayCurrentMonth():
    # Clear out table
    for record in budgetTree.get_children():
            budgetTree.delete(record)

    expenses = db.child('userList').child(activeUser).child('expenses').get()
    for expense in expenses:
        d = expense.val()['date']
        n = expense.val()['name']
        p = expense.val()['planned']
        a = expense.val()['actual']
        m = expense.val()['notes']
        if d[:2] == viewMonth:
            tempTuple = toTuple(d, n, p, a, m)
            budgetTree.insert(parent = '', index = 'end', iid = expense.key(), values = tempTuple)


   
displayCurrentMonth()

# Pack table
budgetTree.pack()

#endregion

#region ===== Button functions ====== #

# Open add entry window
def openAddMenu():

    # Configuration
    top = Toplevel()
    top.geometry("%dx%d" % (sx*.25, sy*0.6))
    top.config(background = accentColor)
    addCal = Calendar(top, selectmode = 'day', year = 2021, month = 6, day = 22, date_pattern = 'mm/dd/yyyy')
    addCal.grid(row = 0, column = 0, pady = 20, padx = 20, columnspan = 2, rowspan = 3)

    # Entry variables
    global monthEntry, dayEntry, yearEntry
    global nameEntry, plannedEntry, actualEntry, notesEntry
    
    selDateLabel = Label(top, text = "Selected Date: __/__/__", bg = accentColor)
    selDateLabel.grid(row = 1, column = 2, columnspan = 2, pady = 10, sticky = E)

    # Grab date from the calendar
    def grabDate():
        global monthEntry, dayEntry, yearEntry
        selectedDate = addCal.get_date()
        selDateLabel.config(text = selectedDate)
        monthEntry = selectedDate[:2]
        dayEntry = selectedDate[3:5]
        yearEntry = selectedDate[-4:]

    # Buttons, labels, and entry widgets
    getDateButton = Button(top, text = "Use this date", command = grabDate)
    getDateButton.grid(row = 0, column = 2, rowspan = 2, columnspan = 2)

    nameLabel = Label(top, text = "Name:", bg = accentColor)
    plannedLabel = Label(top, text = "Planned:", bg = accentColor)
    actualLabel = Label(top, text = "Actual:", bg = accentColor)
    notesLabel = Label(top, text = "Notes:", bg = accentColor)

    nameLabel.grid(row = 3, column = 0, pady = 10)
    plannedLabel.grid(row = 4, column = 0, pady = 10)
    actualLabel.grid(row = 5, column = 0, pady = 10)
    notesLabel.grid(row = 6, column = 0, pady = 10)

    nameEntry = Entry(top)
    plannedEntry = Entry(top)
    actualEntry = Entry(top)
    notesEntry = Entry(top)

    nameEntry.grid(row = 3, column = 1, pady = 10)
    plannedEntry.grid(row = 4, column = 1, pady = 10)
    actualEntry.grid(row = 5, column = 1, pady = 10)
    notesEntry.grid(row = 6, column = 1, pady = 10)
    
    # Add expense to table
    def addExpense():

        # Format date and get other params
        date = monthEntry + "/" + dayEntry + "/" + yearEntry
        n = nameEntry.get()
        p = plannedEntry.get()
        a = actualEntry.get()
        m = notesEntry.get()

        # Format data for additions into table/DB
        tempTuple = toTuple(date, n, p, a, m)
        data = {'date': date, 'name': n, 'planned': p, 'actual': a, 'notes': m, 'category': ""}

        # Insert entry into DB and table
        tempIID = db.child("userList").child('test').child('expenses').push(data)
        budgetTree.insert(parent = '', index = 'end', iid = tempIID['name'], values = tempTuple)

        # Update Table
        displayCurrentMonth()
        top.destroy()

    # Add entry and cancel buttons
    addEntryButton = Button(top, text = "Add Entry", command = addExpense)
    addEntryButton.grid(row = 3, column = 3, rowspan = 2, columnspan = 3, ipadx = 30, ipady = 20, pady = 10, sticky = NW)

    cancelAddButton = Button(top, text = "Cancel", command = lambda: top.destroy())
    cancelAddButton.grid(row = 5, column = 3, rowspan = 2, columnspan = 3, ipadx = 30, ipady = 20, pady = 10, sticky = NW)


# Open update window
def openUpdateMenu():
    # Configuration
    utop = Toplevel()
    utop.geometry("%dx%d" % (sx*.25, sy*0.6))
    utop.config(background = accentColor)

    # Get entries
    global umonthEntry, udayEntry, uyearEntry
    global unameEntry, uplannedEntry, uactualEntry, unotesEntry
    
    selDateLabel = Label(utop, text = "Selected Date: __/__/__", bg = accentColor)
    selDateLabel.grid(row = 1, column = 2, columnspan = 2, pady = 10, sticky = E)

    # Get date from calendar
    def grabDate():
        global umonthEntry, udayEntry, uyearEntry
        selectedDate = updCal.get_date()
        selDateLabel.config(text = selectedDate)
        umonthEntry = selectedDate[:2]
        udayEntry = selectedDate[3:5]
        uyearEntry = selectedDate[-4:]

    # Buttons, labels and entry widgets
    getDateButton = Button(utop, text = "Use this date", command = grabDate)
    getDateButton.grid(row = 0, column = 2, rowspan = 2, columnspan = 2)

    nameLabel = Label(utop, text = "Name:", bg = accentColor)
    plannedLabel = Label(utop, text = "Planned:", bg = accentColor)
    actualLabel = Label(utop, text = "Actual:", bg = accentColor)
    notesLabel = Label(utop, text = "Notes:", bg = accentColor)

    nameLabel.grid(row = 3, column = 0, pady = 10)
    plannedLabel.grid(row = 4, column = 0, pady = 10)
    actualLabel.grid(row = 5, column = 0, pady = 10)
    notesLabel.grid(row = 6, column = 0, pady = 10)

    unameEntry = Entry(utop)
    uplannedEntry = Entry(utop)
    uactualEntry = Entry(utop)
    unotesEntry = Entry(utop)

    unameEntry.grid(row = 3, column = 1, pady = 10)
    uplannedEntry.grid(row = 4, column = 1, pady = 10)
    uactualEntry.grid(row = 5, column = 1, pady = 10)
    unotesEntry.grid(row = 6, column = 1, pady = 10)

    # Grab currently selected values
    selected = budgetTree.focus()
    tempValues = budgetTree.item(selected, 'values')

    # Insert the current values into entry boxes
    unameEntry.insert(0, tempValues[1])
    uplannedEntry.insert(0, tempValues[2].replace('$',''))
    uactualEntry.insert(0, tempValues[3].replace('$',''))
    unotesEntry.insert(0, tempValues[5])

    # Parse data to set calendar
    tm, td, ty = tempValues[0].split(sep = '/')

    updCal = Calendar(utop, selectmode = 'day', year = int(ty), month = int(tm), day = int(td), date_pattern = 'mm/dd/yyyy')
    updCal.grid(row = 0, column = 0, pady = 20, padx = 20, columnspan = 2, rowspan = 3)

    # Grab the new date
    grabDate()

    # Update entry in table
    def updateExpense():
        selected = budgetTree.focus()
        date = umonthEntry + "/" + udayEntry + "/" + uyearEntry
        n = unameEntry.get()
        p = uplannedEntry.get()
        a = uactualEntry.get()
        m = unotesEntry.get()

        # Format data
        tempTuple = toTuple(date, n, p, a, m)
        data = {'date': date, 'name': n, 'planned': p, 'actual': a, 'notes': m, 'category': ""}

        # Update the database record
        for record in budgetTree.selection():
            item = budgetTree.item(record)
            iid = budgetTree.focus()
            for exp in db.child('userList').child(activeUser).child('expenses').get():
                db.child('userList').child(activeUser).child('expenses').child(iid).update(data)
        
        # Update table and destroy "update" window
        budgetTree.item(selected, text = "", values = tempTuple)
        displayCurrentMonth()
        utop.destroy()

    # Update/cancel button widgets
    updateButton = Button(utop, text = "Update Entry", command = updateExpense)
    updateButton.grid(row = 3, column = 3, rowspan = 2, columnspan = 3, ipadx = 30, ipady = 20, pady = 10, sticky = W)

    cancelAddButton = Button(utop, text = "Cancel", command = lambda: utop.destroy())
    cancelAddButton.grid(row = 5, column = 3, rowspan = 2, columnspan = 3, ipadx = 45, ipady = 20, pady = 10, sticky = W)


# Remove expense
def deleteExpense():
    # In the selection from table
    for expense in budgetTree.selection():

        # Get the iid (unique database key for the expense)
        item = budgetTree.item(expense)
        iid = budgetTree.focus()
        # Popup to confirm action
        c = messagebox.askokcancel("Warning", "Are you sure you want to delete selected item(s)? (This cannot be undone)")

        # If action approved
        if c:
            # Delete unique expense from database
            for record in budgetTree.selection():
                item = budgetTree.item(record)
                iid = budgetTree.focus()
                for exp in db.child('userList').child(activeUser).child('expenses').get():
                    # Make sure the key in DB matches the iid
                    if exp.key() == iid:
                        db.child("userList").child(activeUser).child('expenses').child(iid).remove()
                        print(iid, exp.key())
                budgetTree.delete(record)


# Export file as xlsx
def export():
    newXS = xw.Workbook('HELLO THERE.xlsx')
    s1 = newXS.add_worksheet('Current Month')
    rnum = 1
    cnum = 0
    messagebox.showinfo("File Alert", "Excel file has been created!")

    bold = newXS.add_format({'bold': True})
    s1.write(rnum, cnum + 1, "Date", bold)
    s1.write(rnum, cnum + 2, "Name", bold)
    s1.write(rnum, cnum + 3, "Planned", bold)
    s1.write(rnum, cnum + 4, "Actual", bold)
    s1.write(rnum, cnum + 5, "Difference", bold)
    s1.write(rnum, cnum + 6, "Notes", bold)
    rnum += 1

    # For ALL expenses in DB with correct month
    for expense in db.child('userList').child(activeUser).child('expenses').get():
        print(expense.val()['actual'])
        if expense.val()['date'][:2] == viewMonth:
            s1.write(rnum, cnum + 1, expense.val()['date'])
            s1.write(rnum, cnum + 2, expense.val()['name'])
            s1.write(rnum, cnum + 3, float(expense.val()['planned']))
            s1.write(rnum, cnum + 4, float(expense.val()['actual']))
            s1.write(rnum, cnum + 5, float(expense.val()['planned'])-float(expense.val()['actual']))
            s1.write(rnum, cnum + 6, expense.val()['notes'])
            rnum += 1

    newXS.close()

#endregion ButtonFunctions

#region Main Entry Buttons
addButton = Button(tableFrame, text = "Add expense", command = openAddMenu, font = usernameFont, height = 4, width = 15)
addButton.grid(row = 3, column = 0, pady = 20)
addButton.config(bg = '#40c25c')

updateButton = Button(tableFrame, text = "Edit Entry", font = usernameFont, command = openUpdateMenu, height = 4, width = 15)
updateButton.grid(row = 3, column = 2, pady = 20)
updateButton.config(bg = '#e0be36')

removeButton = Button(tableFrame, text = "Delete Entry", font = usernameFont, command = deleteExpense, height = 4, width = 15)
removeButton.grid(row = 3, column = 4, pady = 20)
removeButton.config(bg = '#d14232')

convertButton = Button(budgetFrame, text = "Convert", command = export, font = usernameFont, height = 3, width = 15, bg = accentColor)
convertButton.grid(row = 0, column = 0, pady = 0)

# Formatting (font changes)
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 12))
style.configure("Treeview", font = ("Verdana", 16), rowheight = 50)

#endregion

root.mainloop()