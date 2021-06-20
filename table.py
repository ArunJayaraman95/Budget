# Imports
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
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


# Configurations
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

loginFrame = Frame(root, background = mainColor)
registerFrame = Frame(root, background = mainColor)

for frame in (loginFrame, registerFrame):
    frame.grid(row = 0, column = 0, sticky = "nsew")

showFrame(registerFrame)

sx = root.winfo_screenwidth() 
sy = root.winfo_screenheight()

# Set the window size
root.geometry("%dx%d" % (sx, sy))
root.title("Budget Boi")
root.iconbitmap("img/WayneStateLogo.ico")

#region Frame1
#============Frame 1 ==============# 
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
#loginMenu.grid(row = 0, column = 0, padx = sx * widthAdjuster, pady = sy * heightAdjuster, ipadx = 0, ipady = 0)
#loginMenu.place(height = 500, width = 400, anchor = CENTER, rely = 0.5, relx = 0.5)
loginMenu.pack()
loginMenu.config()
# Labels
loginTitle = Label(loginMenu, text = "Login", font = ("Courier", 80), bg = accentColor)
loginTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")

#endregion


root.mainloop()