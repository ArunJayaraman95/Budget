# Imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
from tkcalendar import *
import re
import smtplib, ssl
import random, string
from typing import ContextManager
import xlsxwriter as xw
import pyrebase

# Firebase Configuration
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
mainColor = "#56C3A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 20)
inputFont = ("Verdana", 16)
usernameFont = ("Verdana", 12)

def showFrame(frame_1):
    frames =[loginFrame, registerFrame, twoFactorFrame, forgotFrame, homeFrame, budgetFrame]
    frames.remove(frame_1)
    for frame in frames:
        frame.lower()
    frame_1.lift()

# Creating window
root=Tk()
root.state("zoomed")  #Makes it fullscreen automatically


# Configurations
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

# Frames
loginFrame = Frame(root, background = mainColor)
registerFrame = Frame(root, background = mainColor)
homeFrame = Frame(root, background = mainColor)
twoFactorFrame = Frame(root, background = mainColor)
forgotFrame = Frame(root, background = mainColor)
budgetFrame = Frame(root, background = mainColor)


for frame in (loginFrame, registerFrame, twoFactorFrame, forgotFrame, budgetFrame, homeFrame):
    frame.grid(row = 0, column = 0, sticky = "nsew")


showFrame(loginFrame)

sx = root.winfo_screenwidth() 
sy = root.winfo_screenheight()

# Set the window size
root.geometry("%dx%d" % (sx, sy))
root.title("Budget Boi")
root.iconbitmap("img/WayneStateLogo.ico")

#region===========Login Frame 1 ==============# 
# Variables
activeUser = ""



# Functions

generatedCode = ""

def logoutPressed():
    global activeUser
    showFrame(loginFrame)
    activeUser = ""

def showhome():
    showFrame(homeFrame)

'''
def forgotPassword():
    showFrame(forgotFrame)
    passEntry = pInput.get()
    foundFlag = False
    foundEmail = ""
    # Check username
    print("Userentry", userEntry, uInput.get())
    with open('UserData/userList.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            print(line)
            if line[0].lower().strip() == userEntry.lower():
                print("In file")
                foundFlag = True
                activeUser = userEntry
                foundEmail  = line[2].lower().strip();
                #messagebox.showinfo("Success!", "Welcome " + activeUser + "!")
                
                showFrame(forgotFrame)
                global generatedPasswordCode
                generatedPasswordCode = SendResetCode(foundEmail)
                print(generatedPasswordCode)
                return
                #break
        if not foundFlag:
            print("Username (" + userEntry + ") not found")
            messagebox.showwarning("Warning", "User not found")         
    uInput.delete(0, END)
    pInput.delete(0, END)
    print("Active user:", activeUser)
'''

def submitLogin():
    global activeUser
    #print("Login submit button clicked")
    userEntry = uInput.get().lower()
    passEntry = pInput.get()

    # Check credentials
    #print("Userentry", userEntry, uInput.get())
    users = db.child('userList').get()
    found = False
    for user in users:
        if user.val()['username'] == userEntry:
            found = True
            try:
                auth.sign_in_with_email_and_password(user.val()['email'], passEntry)
                messagebox.showinfo("Welcome!", "Signed in!")
                activeUser = userEntry
                showFrame(budgetFrame)
                displayCurrentMonth()
            except:
                messagebox.showwarning("Warning", "Error occurred")
    if found == False:
      messagebox.showwarning("Warning", "Invalid credentials")

        
    uInput.delete(0, END)
    pInput.delete(0, END)
    #print("Active user:", activeUser)
    # Clear inputs



def processUserEnteredCode():
    #print("Register account clicked")
    global generatedCode

    # Store entries
    userCodeEntry = ecInput.get()
    if userCodeEntry != generatedCode:
        messagebox.showwarning("Invalid", "Please check the code in the email")
    else:
        messagebox.showwarning("Hooray", "Hooray!!")
        
         
        showhome()


def processForgotCode():
    global generatedPasswordCode
    # Store entries
    userCodeEntry = ecResetInput.get()
    passResetEntry = prResetInput.get()
    confResetEntry = pcResetInput.get()
    
    if passResetEntry != confResetEntry:
        messagebox.showwarning("Invalid", "Passwords do not match")
    elif userCodeEntry != generatedPasswordCode:
        messagebox.showwarning("Invalid", "Please check the code in the email")
    elif len(passResetEntry) >= 8 and uppercase_check(passResetEntry) and lowercase_check(passResetEntry) and digit_check(passResetEntry):
        changePassword(passResetEntry)
        messagebox.showwarning("Hooray", "Password has been updated.")
        showFrame(loginFrame) 
    else:
        messagebox.showwarning("Alarm", "Password is weak \n Password Must be in \n 1) Minimum 8 characters.\n 2) The alphabets must be between [a-z].\n 3) At least one alphabet should be of Upper Case [A-Z].\n 4) At least 1 number or digit between [0-9].")
   

##test stuff

# REFACTOR
def changePassword(newPassword):
    global savedUsername
    infile = open('UserData/userList.csv', 'r')
    newText = ""
    content = infile.readlines()
    for line in content:
        if savedUsername in line: ####
            newText += line.split(",")[0]+","+newPassword +","+line.split(",")[2]
        else:
            newText += line 
    infile.close()

    outfile = open('UserData/userList.csv', 'w')
    outfile.write(newText)
    outfile.close()


global savedUsername
savedUsername ="ddddd"
changePassword("bbbbb")
 
# Create subframe
widthAdjuster = 0.4
heightAdjuster = 0.2
loginMenu = Frame(loginFrame, bg = accentColor)
loginMenu.pack()
loginMenu.config()
# Labels
loginTitle = Label(loginMenu, text = "Login", font = ("Courier", 80), bg = accentColor)
loginTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")

usernameLabel = Label(loginMenu, text = "Username:", font = usernameFont, bg = accentColor)
usernameLabel.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = "w")

passwordLabel = Label(loginMenu, text = "Password: ", font = usernameFont, bg = accentColor)
passwordLabel.grid(row = 3, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'w')

# Create entry boxes
uInput = Entry(loginMenu, width = 20, font = inputFont)
uInput.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

pInput = Entry(loginMenu, width = 20, font = inputFont, show = '*')
pInput.grid(row = 4, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

# Create buttons
forgotButton = Button(loginMenu, text = "Forgot Password", bg = "#A9e451", padx = 10, pady = 0, font = ("Verdana", 15), command = lambda: showFrame(forgotFrame)) #code here for new frame
forgotButton.grid(row = 5, column = 0, padx = 20, pady = 10, sticky = 'ew')
submitButton = Button(loginMenu, text = "Submit", bg = "#A9e451", padx = 10, pady = 0, font = ("Verdana", 15), command = submitLogin) #code here for new frame
submitButton.grid(row = 5, column = 1, padx = 20, pady = 10, sticky = 'ew')
registerButton = Button(loginMenu, text = "Make new account", font = ("Verdana", 10), bg = mainColor, command = lambda: showFrame(registerFrame))
registerButton.grid(row = 6, column = 0, padx = 20, pady = 10, sticky = 'ew')

#endregion

#region ===============RegisterAccount Frame 2=====================#

def uppercase_check(passEntry):
    if re.search('[A-Z]', passEntry): #atleast one uppercase character
        return True
    return False

def lowercase_check(passEntry):
    if re.search('[a-z]', passEntry): #atleast one lowercase character
        return True
    return False

def digit_check(passEntry):
    if re.search('[0-9]', passEntry): #atleast one digit
        return True
    return False

def check(email):   
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
    # REFACTOR 
    if(re.search(regex,email)):
        return True
    else:
        return False 

# Functions
def registerAccount():
    #print("Register account clicked")

    # Store entries
    userEntry = urInput.get().lower()
    emailEntry = emInput.get()
    passEntry = prInput.get()
    confEntry = pcInput.get()
    foundFlag = False

    # Check username
    userDB = db.child('userList').child(userEntry).get()
    if userDB.val():
        #print(userDB)
        foundFlag = True
                

    if not foundFlag:
        if not check(emailEntry):
            messagebox.showwarning("Alarm", "Invalid Email")
            
        elif passEntry != confEntry:
            messagebox.showwarning("Error", "Passwords don't match")
        # Good case
        elif len(passEntry) >= 8 and uppercase_check(passEntry) and lowercase_check(passEntry) and digit_check(passEntry):
            messagebox.showwarning("Alarm", "Password is strong")
 
            try:
                auth.create_user_with_email_and_password(emailEntry, passEntry)
                #print("Account made")
                #print("User ", userEntry, "added!")
                messagebox.showinfo("Success!", "User added!")
                data = {'email': emailEntry, 'password': passEntry, 'username': userEntry}
                db.child('userList').child(userEntry).set(data)
            except:
                #print("Email already exists")
                messagebox.showwarning("Invalid", "Username or email is already in use. Try again.")

            
        else:
            messagebox.showwarning("Alarm", "Password is weak \n Password Must be in \n 1) Minimum 8 characters.\n 2) The alphabets must be between [a-z].\n 3) At least one alphabet should be of Upper Case [A-Z].\n 4) At least 1 number or digit between [0-9].")
    else:
        messagebox.showwarning("Invalid", "Username or email is already in use. Try again.")
    urInput.delete(0, END)
    emInput.delete(0, END)
    prInput.delete(0, END)
    pcInput.delete(0, END)



widthAdjuster2 = 0.37
heightAdjuster2 = 0.2
registerMenu = Frame(registerFrame, bg = accentColor)
#registerMenu.grid(row = 0, column = 0, padx = sx * widthAdjuster2, pady = sy * heightAdjuster2, ipadx = 0, ipady = 0)
registerMenu.place(height = 600, width = 500, anchor = CENTER, rely = 0.5, relx = 0.5)


# Create labels for login and place them
registerTitle = Label(registerMenu, text = "Register!", font = ("Courier", 60), bg = accentColor)
registerTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")

usernameLabel = Label(registerMenu, text = "Username: ", font = usernameFont, bg = accentColor)
usernameLabel.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = "w")

emailLabel = Label(registerMenu, text = "Email: ", font = usernameFont, bg = accentColor)
emailLabel.grid(row = 3, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'w')

passwordLabel = Label(registerMenu, text = "Password: ", font = usernameFont, bg = accentColor)
passwordLabel.grid(row = 5, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'w')

passwordConLabel = Label(registerMenu, text = "Confirm Password: ", font = usernameFont, bg = accentColor)
passwordConLabel.grid(row = 7, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'w')


# Create input box for username and password
urInput = Entry(registerMenu, width = 20, font = inputFont)
urInput.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

emInput = Entry(registerMenu, width = 20, font = inputFont)
emInput.grid(row = 4, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

prInput = Entry(registerMenu, width = 20, font = inputFont, show = '*')
prInput.grid(row = 6, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

pcInput = Entry(registerMenu, width = 20, font = inputFont, show = '*')
pcInput.grid(row = 8, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')


#Create buttons
confirmButton = Button(registerMenu, text = "Register", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = registerAccount)#here code
confirmButton.grid(row = 10, column = 1, padx = 20, pady = 10, sticky = 'ew')

returnButton = Button(registerMenu, text = "Return to login", font = ("Verdana", 10), bg = mainColor, command = lambda: showFrame(loginFrame))
returnButton.grid(row = 10, column = 0, padx = 20, pady = 10, sticky = 'ew')

#endregion
#================Home Page Setup=================================#

homeMenu = Frame(homeFrame, bg = accentColor)
homeMenu.place(height = 600, width = 500, anchor = CENTER, rely = 0.5, relx = 0.5)
homeTitle = Label(homeMenu, text = "Home", font = ("Courier", 60), bg = accentColor)
homeTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")
homeLogOutButton = Button(budgetFrame, text = "Log Out", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = logoutPressed)
homeLogOutButton.grid(row = 8, column = 0, padx = 20, pady = 10, sticky = 'ew')


#region===============TwoFactorCode Frame 3=====================#

def randomword(length):
   letters = "1234567890abcdefghijklmnopqrstuvwxyz"
   return ''.join(random.choice(letters) for i in range(length))

port = 465  # For SSL
#password = input("Type your password and press enter: ")

# Create a secure SSL context
context = ssl.create_default_context()

def SendTwoFactorCode(email_recipent):
    code = randomword(10)
    #do to make code random


    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "robiakther007@gmail.com"  # Enter your address
    receiver_email = email_recipent # Enter receiver address
    password = "ra101112"
    message = """\
    Subject: Authentication Code

    Your two factor authentication code is """+ code + "."

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return code

def SendResetCode(email_recipent):
    code = randomword(10)
    #do to make code random


    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "robiakther007@gmail.com"  # Enter your address
    receiver_email = email_recipent # Enter receiver address
    password = "ra101112"
    message = """\
    Subject: Password Reset Code

    The code to reset your password is """+ code + "."

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return code

widthAdjuster2 = 0.37
heightAdjuster2 = 0.2


#New Frame
resetMenu = Frame(forgotFrame, bg = accentColor)
resetMenu.place(height = 600, width = 500, anchor = CENTER, rely = 0.5, relx = 0.5)
# Create labels for resetMenun
resetTitle = Label(resetMenu, text = "Forgot Password", font = ("Courier", 20), bg = accentColor)
resetTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")

enterresetcodeLabel = Label(resetMenu, text = "Enter email to send reset link to: ", font = usernameFont, bg = accentColor)
enterresetcodeLabel.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = "w")

# Create input box for Enter code
ecResetInput = Entry(resetMenu, width = 15, font = inputFont)
ecResetInput.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

def attemptReset():
    try:
        auth.send_password_reset_email(ecResetInput.get())
        doneResetButton.config(text = "Send Again")
        messagebox.showinfo("Sent", "Your email containing a link to reset your password has been sent!")
    except:
        messagebox.showwarning("Error", "Email may be invalid. Try again.")
        ecResetInput.delete(0, END)

def returnToLogin():
    showFrame(loginFrame)
#Create buttons
doneResetButton = Button(resetMenu, text = "Back", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = returnToLogin)
doneResetButton.grid(row = 7, column = 0, padx = 20, pady = 10, sticky = 'ew')

doneResetButton = Button(resetMenu, text = "Send", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = attemptReset)
doneResetButton.grid(row = 7, column = 1, padx = 20, pady = 10, sticky = 'ew')

#New Frame
factorMenu = Frame(twoFactorFrame, bg = accentColor)
factorMenu.place(height = 600, width = 500, anchor = CENTER, rely = 0.5, relx = 0.5)
# Create labels for Two-Factor Authentication
twoFactorTitle = Label(factorMenu, text = "Two-Factor Authentication", font = ("Courier", 60), bg = accentColor)
twoFactorTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")

entercodeLabel = Label(factorMenu, text = "Enter code: ", font = usernameFont, bg = accentColor)
entercodeLabel.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = "w")

# Create input box for Enter code
ecInput = Entry(factorMenu, width = 15, font = inputFont)
ecInput.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

#Create buttons
doneButton = Button(factorMenu, text = "Done", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = processUserEnteredCode)
doneButton.grid(row = 3, column = 0, padx = 20, pady = 10, sticky = 'ew')

#endregion

#region=============Table Frame 4 ==========#


# Variables
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
def updateTable(vm):
    global viewMonth
    try:
        if int(vm) >= 1 and int(vm) <= 12:
            if len(vm) == 1:
                vm = '0' + vm
            viewMonth = vm
            displayCurrentMonth()
            return 0
        return -1
    except:
        messagebox.showwarning("Invalid Input!", "Month must be an integer from 1 to 12")
        return -1

confirmViewMonth = Button(budgetFrame, text = "View", command = lambda: updateTable(viewMonthEntry.get()))
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



# Generate tuple from data for updates/insertions
# This removes dollar signs and commas from monatory values
def toTuple(date, name, planned, actual, notes = ""):
    try:
        a = date
        b = str(name)
        c = '${:,.2f}'.format(float(planned)) 
        d = '${:,.2f}'.format(float(actual)) 
        e = round(float(planned) - float(actual), 2)
        e = '-${:,.2f}'.format(-e) if e < 0 else '${:,.2f}'.format(e)
        if notes:
            f = notes
        else:
            f = ""
        return (a, b, c, d, e, f)
    except:
        print("Error in tuple input")
        return -1

def displayCurrentMonth():
    # Clear out table
    try:
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
    except:
        pass
        #print("No stuff in tree")

   
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
        return [monthEntry, dayEntry, yearEntry]

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
        tempIID = db.child("userList").child(activeUser).child('expenses').push(data)
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
    uplannedEntry.insert(0, tempValues[2].replace('$','').replace(',',''))
    uactualEntry.insert(0, tempValues[3].replace('$','').replace(',',''))
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
                        #print(iid, exp.key())
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
        #print(expense.val()['actual'])
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
convertButton.grid(row = 0, column = 0, pady = 10)

# Formatting (font changes)
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 12))
style.configure("Treeview", font = ("Verdana", 16), rowheight = 50)

#endregion

#endregion
def grabDate(selectedDate):
    monthEntry = selectedDate[:2]
    dayEntry = selectedDate[3:5]
    yearEntry = selectedDate[-4:]
    return [monthEntry, dayEntry, yearEntry]

root.mainloop()