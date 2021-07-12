# Imports
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import re
#from PIL import ImageTk, Image
import csv
import smtplib, ssl
import random, string

# Define colors
mainColor = "#56C3A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 20)
inputFont = ("Verdana", 16)
usernameFont = ("Verdana", 12)

def showFrame(frame):
    frame.tkraise()

# Creating window
root=Tk()
root.state("zoomed")  #Makes it fullscreen automatically


# Configurations
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

loginFrame = Frame(root, background = mainColor)
registerFrame = Frame(root, background = mainColor)
twoFactorFrame = Frame(root, background = mainColor)

for frame in (loginFrame, registerFrame, twoFactorFrame):
    frame.grid(row = 0, column = 0, sticky = "nsew")

showFrame(registerFrame)

sx = root.winfo_screenwidth() 
sy = root.winfo_screenheight()

# Set the window size
root.geometry("%dx%d" % (sx, sy))
root.title("Budget Boi")
root.iconbitmap("img/WayneStateLogo.ico")

#region Frame1
#============Login Frame 1 ==============# 
# Variables
activeUser = ""

# Functions
def submitLogin():
    global activeUser
    print("Login submit button clicked")
    userEntry = uInput.get()
    passEntry = pInput.get()
    foundFlag = False
    # Check username
    print("Userentry", userEntry, uInput.get())
    with open('UserData/userList.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            print(line)
            if line[0].lower().strip() == userEntry.lower() and line[1].strip() == passEntry:
                print("In file")
                foundFlag = True
                activeUser = userEntry
                messagebox.showinfo("Success!", "Welcome " + activeUser + "!")

                #here
                #code = SendTwoFactorCode("ffddfdf@dfdsf.com")
                #steps
                #build frame with input box and button
                #show two factor authentication input box in frame
                #add event trigger to button that when pressed chechs user input == code
                #if UserAuthCode == code:
                    #Leave
                #else:
                    #show error
                
                break
        if not foundFlag:
            print("Username (" + userEntry + ") not found")
            messagebox.showwarning("User not found")
            #warningLabel = Label(loginMenu, text = "Incorrect credentials", fg = "#FF890A", bg = accentColor)
            #warningLabel.config(font = ("Verdana", 12))
            #warningLabel.grid(row = 6, column = 1)
    uInput.delete(0, END)
    pInput.delete(0, END)
    print("Active user:", activeUser)

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
submitButton = Button(loginMenu, text = "Submit", bg = "#A9e451", padx = 10, pady = 0, font = ("Verdana", 15), command = submitLogin)
submitButton.grid(row = 5, column = 1, padx = 20, pady = 10, sticky = 'ew')
registerButton = Button(loginMenu, text = "Make new account", font = ("Verdana", 10), bg = mainColor, command = lambda: showFrame(registerFrame))
registerButton.grid(row = 6, column = 0, padx = 20, pady = 10, sticky = 'ew')

#endregion

# ===============RegisterAccount Frame 2=====================#
#####################################################################################################


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
    if(re.search(regex,email)):
        return True
    else:
        return False 
#####################################################################################################



# Functions
def registerAccount():
    print("Register account clicked")

    # Store entries
    userEntry = urInput.get()
    emailEntry = emInput.get()
    passEntry = prInput.get()
    confEntry = pcInput.get()
    foundFlag = False

    # Check username
    with open('UserData/userList.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            print(line)
            if line[0].lower().strip() == userEntry.lower():
                print("User already exists")
                foundFlag = True
                

        if not foundFlag:
            
            if not  check(emailEntry):
                    messagebox.showwarning("Alarm", "Invalid Email")
               
            elif passEntry != confEntry:
                messagebox.showwarning("Error", "Passwords don't match")

            elif len(passEntry) >= 8 and uppercase_check(passEntry) and lowercase_check(passEntry) and digit_check(passEntry):
                messagebox.showwarning("Alarm", "Password is strong")
                with open ('UserData/userList.csv', 'a') as file:
                    writer = csv.writer(file, lineterminator="\n")
                    writer.writerow([userEntry, passEntry])
                print("User ", userEntry, "added!")
                messagebox.showinfo("Success!", "User added!")

                #to do move into success section
                code = SendTwoFactorCode(emailEntry)
                #steps
                #build frame with input box and button
                #show two factor authentication input box in frame
                #add event trigger to button that when pressed chechs user input == code
                #if UserAuthCode == code:
                    #Leave
                #else:
                    #show error



        




            
            else:
                messagebox.showwarning("Alarm", "Password is weak \n Password Must be in \n 1) Minimum 8 characters.\n 2) The alphabets must be between [a-z].\n 3) At least one alphabet should be of Upper Case [A-Z].\n 4) At least 1 number or digit between [0-9].")

  

   
    urInput.delete(0, END)
    emInput.delete(0,END)
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
confirmButton = Button(registerMenu, text = "Register", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = registerAccount)
confirmButton.grid(row = 10, column = 1, padx = 20, pady = 10, sticky = 'ew')

returnButton = Button(registerMenu, text = "Return to login", font = ("Verdana", 10), bg = mainColor, command = lambda: showFrame(loginFrame))
returnButton.grid(row = 10, column = 0, padx = 20, pady = 10, sticky = 'ew')

# ===============TwoFactorCode Frame 3=====================#

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
    Subject: Hi there

    Your two factor authentication code is """+ code + "."

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return code

widthAdjuster2 = 0.37
heightAdjuster2 = 0.2

factorMenu = Frame(twoFactorFrame, bg = accentColor)
factorMenu.place(height = 600, width = 500, anchor = CENTER, rely = 0.5, relx = 0.5)
# Create labels for Two-Factor Authentication
twoFactorTitle = Label(factorMenu, text = "Two-Factor Authentication", font = ("Courier", 60), bg = accentColor)
twoFactorTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")

entercodeLabel = Label(factorMenu, text = "Enter code: ", font = usernameFont, bg = accentColor)
entercodeLabel.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = "w")

# Create input box for Enter code
ecInput = Entry(factorMenu, width = 20, font = inputFont)
ecInput.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

#Create buttons
doneButton = Button(factorMenu, text = "Done", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = registerAccount)
doneButton.grid(row = 3, column = 1, padx = 20, pady = 10, sticky = 'ew')
root.mainloop()