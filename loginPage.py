# Imports
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import re
from PIL import ImageTk, Image
import csv
import smtplib, ssl
import random, string
from typing import ContextManager

# Define colors
mainColor = "#56C3A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 20)
inputFont = ("Verdana", 16)
usernameFont = ("Verdana", 12)

def showFrame(frame_1):
    frames =[loginFrame, registerFrame, twoFactorFrame, forgotFrame, homeFrame]
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

loginFrame = Frame(root, background = mainColor)
registerFrame = Frame(root, background = mainColor)
homeFrame = Frame(root, background = mainColor)
twoFactorFrame = Frame(root, background = mainColor)
forgotFrame = Frame(root, background = mainColor)

for frame in (loginFrame, registerFrame, twoFactorFrame, forgotFrame, homeFrame):
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



#Functions

def logoutPressed():
    global activeUser
    showFrame(loginFrame)
    activeUser = ""

def showhome():
    showFrame(homeFrame)


def forgotPassword():
    global activeUser
    global savedUsername
    print("Login submit button clicked")
    userEntry = uInput.get()
    savedUsername = userEntry


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
                loginFrame.grid_forget()#Hide/destroy the registerframe
                showFrame(forgotFrame)
                global generatedPasswordCode
                generatedPasswordCode = SendResetCode(foundEmail)
                return
                #break
        if not foundFlag:
            print("Username (" + userEntry + ") not found")
            messagebox.showwarning("Warning", "User not found")         
    uInput.delete(0, END)
    pInput.delete(0, END)
    print("Active user:", activeUser)

def submitLogin():
    global activeUser
    print("Login submit button clicked")
    userEntry = uInput.get()
    passEntry = pInput.get()
    foundFlag = False
    foundEmail = ""
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
                foundEmail  = line[2].lower().strip();
                #messagebox.showinfo("Success!", "Welcome " + activeUser + "!")
                registerFrame.grid_forget()#Hide/destroy the registerframe
                showFrame(twoFactorFrame)
                global generatedCode
                generatedCode = SendTwoFactorCode(foundEmail)
                break
        if not foundFlag:
            print("Username (" + userEntry + ") not found")
            messagebox.showwarning("Warning", "User not found")         
    uInput.delete(0, END)
    pInput.delete(0, END)
    print("Active user:", activeUser)




def processUserEnteredCode():
    print("Register account clicked")
    global generatedCode
    # Store entries
    userCodeEntry = ecInput.get()
    if userCodeEntry != generatedCode:
        messagebox.showwarning("Invalid", "Please check the code in the email")
    else:
        messagebox.showwarning("Hooray", "Hooray!!")
        
        forgotFrame.grid_forget()#Hide/destroy the forgot frame
        showFrame(loginFrame) 


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
        
        forgotFrame.grid_forget()#Hide/destroy the registerframe
        showFrame(loginFrame) 
    else:
        messagebox.showwarning("Alarm", "Password is weak \n Password Must be in \n 1) Minimum 8 characters.\n 2) The alphabets must be between [a-z].\n 3) At least one alphabet should be of Upper Case [A-Z].\n 4) At least 1 number or digit between [0-9].")
   

##test stuff



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
forgotButton = Button(loginMenu, text = "Forgot Password", bg = "#A9e451", padx = 10, pady = 0, font = ("Verdana", 15), command = forgotPassword) #code here for new frame
forgotButton.grid(row = 5, column = 0, padx = 20, pady = 10, sticky = 'ew')
submitButton = Button(loginMenu, text = "Submit", bg = "#A9e451", padx = 10, pady = 0, font = ("Verdana", 15), command = submitLogin) #code here for new frame
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
                    writer.writerow([userEntry, passEntry,emailEntry])
                print("User ", userEntry, "added!")
                messagebox.showinfo("Success!", "User added!")

               



        




            
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
confirmButton = Button(registerMenu, text = "Register", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = registerAccount)#here code
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
def SendResetCode(email_recipent):
    code = randomword(10)
    #do to make code random


    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "robiakther007@gmail.com"  # Enter your address
    receiver_email = email_recipent # Enter receiver address
    password = "ra101112"
    message = """\
    Subject: Hi there

    The code to reset your password is """+ code + "."

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return code

widthAdjuster2 = 0.37
heightAdjuster2 = 0.2






#New Frame for Forgot password
resetMenu = Frame(forgotFrame, bg = accentColor)
resetMenu.place(height = 600, width = 500, anchor = CENTER, rely = 0.5, relx = 0.5)
# Create labels for resetMenun
resetTitle = Label(resetMenu, text = "Reset Password Code Sent to Email:", font = ("Courier", 20), bg = accentColor)
resetTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")

enterresetcodeLabel = Label(resetMenu, text = "Enter code: ", font = usernameFont, bg = accentColor)
enterresetcodeLabel.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = "w")

# Create input box for Enter code
ecResetInput = Entry(resetMenu, width = 20, font = inputFont)
ecResetInput.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')



passwordResetLabel = Label(resetMenu, text = "new Password: ", font = usernameFont, bg = accentColor)
passwordResetLabel.grid(row = 3, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'w')

passwordResetConLabel = Label(resetMenu, text = "Confirm new Password: ", font = usernameFont, bg = accentColor)
passwordResetConLabel.grid(row = 5, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'w')

prResetInput = Entry(resetMenu, width = 20, font = inputFont, show = '*')
prResetInput.grid(row = 4, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

pcResetInput = Entry(resetMenu, width = 20, font = inputFont, show = '*')
pcResetInput.grid(row = 6, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')




#Create buttons
doneResetButton = Button(resetMenu, text = "Done", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = processForgotCode)
doneResetButton.grid(row = 7, column = 0, padx = 20, pady = 10, sticky = 'ew')







#New Frame for Two factor
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
doneButton = Button(factorMenu, text = "Done", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = processUserEnteredCode)
doneButton.grid(row = 3, column = 0, padx = 20, pady = 10, sticky = 'ew')
root.mainloop()