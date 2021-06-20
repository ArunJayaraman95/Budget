# Imports
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
import csv



def showFrame(frame):
    frame.tkraise()

# Creating window
root=Tk()
root.state("zoomed")  #Makes it fullscreen automatically

# Define colors
mainColor = "#56C3A2"
accentColor = "#57729E"

# Define fonts
buttonFont = font.Font(size = 24)
inputFont = font.Font(size = 20)

# Configurations
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

loginFrame = Frame(root, background = mainColor)
newAccountFrame = Frame(root, background = mainColor)

for frame in (loginFrame, newAccountFrame):
    frame.grid(row = 0, column = 0, sticky = "nsew")

showFrame(loginFrame)

# Set screen width (sx) and height (sy)
sx = root.winfo_screenwidth() 
sy = root.winfo_screenheight()

# Set the window size
root.geometry("%dx%d" % (sx, sy))
root.title("Budget Boi")
root.iconbitmap("img/WayneStateLogo.ico")

#============Frame 1 ==============# 



# Create canvas
canvas = Canvas(loginFrame, width = sx, height = sy)
canvas.pack()
canvas.config(background=mainColor)

# Form outline
canvas.create_rectangle(sx/2 - 200, sy/6, sx/2 + 200, 2*sy/3-50, fill = accentColor, width = 0)

# Create labels for login and place them
usernameFont = font.Font(size = 16)
usernameLabel = Label(loginFrame, text = "Username: ", font = usernameFont, bg = accentColor)
usernameLabel.place(x = sx/2 - 97, y = sy/2 - 110, anchor = N)
loginLabel = Label(loginFrame, text = "Login", font = usernameFont, bg = accentColor)
loginLabel.place(x = sx/2, y = sy/2 - 350, anchor = N)
loginLabel.config(font = ("Courier", 44))
passwordLabel = Label(loginFrame, text = "Password: ", font = usernameFont, bg = accentColor)
passwordLabel.place(x = sx/2 - 97, y = sy/2 - 40, anchor = N)


# Logo image
#logo = ImageTk.PhotoImage(Image.open("img/Dollar Sign.png").resize((120, 120)))
#logoImage = Label(image = logo)
#logoImage.place(x = sx/2, y = sy/2 - 270, anchor = N)


# Create input box for username and password
uInput = Entry(loginFrame, width = 20, font = inputFont)
uInput.place(x = sx/2, y = sy/2 - 80, anchor = N)
pInput = Entry(loginFrame, width = 20, font = inputFont, show = '*')
pInput.place(x=sx/2, y = sy/2 - 10, anchor = N)



activeUser = ""

def popupLogin(message):
    win = Toplevel()
    win.wm_title("Window")
    win.geometry("+%d+%d" % (sx/2 - 50, sy/2-200))
    l = Label(win, text=message)
    l.grid(row=0, column=0)

    b = Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)


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
                popupLogin("Welcome " + line[0] + "!")
                break
        if not foundFlag:
            print("Username (" + userEntry + ") not found")
            #popupLogin("Username not found")
            warningLabel = Label(loginFrame, text = "Incorrect credentials", fg = "#FF890A", bg = accentColor)
            warningLabel.config(font = ("Verdana", 12))
            warningLabel.place(x = sx/2 - 70, y = sy/2 + 30, anchor = N)
    uInput.delete(0, END)
    pInput.delete(0, END)
    print("Active user:", activeUser)

#Create buttons
submitButton = Button(loginFrame, text = "Submit", bg = "#A9e451", padx = 10, pady = 0, font = ("Verdana", 15), command = submitLogin)
submitButton.place(x = sx/2 + 100, y = sy/2 + 70, anchor = N)
registerButton = Button(loginFrame, text = "Make new account", font = ("Verdana", 10), bg = mainColor, command = lambda: showFrame(newAccountFrame))
registerButton.place(x = sx/2 - 85, y = sy/2 + 80, anchor = N)



# ===============Frame 2=====================#
# Create canvas
canvas = Canvas(newAccountFrame, width = sx, height = sy)
canvas.pack()
canvas.config(background=mainColor)

# Form outline
canvas.create_rectangle(sx/2 - 200, sy/6, sx/2 + 200, 2*sy/3-50, fill = accentColor, width = 0)


# Create labels for login and place them
loginLabel = Label(newAccountFrame, text = "Register!", font = usernameFont, bg = accentColor)
loginLabel.place(x = sx/2, y = sy/2 - 350, anchor = N)
usernameFont = font.Font(size = 16)
usernameLabel = Label(newAccountFrame, text = "Username: ", font = usernameFont, bg = accentColor)
usernameLabel.place(x = sx/2 - 155, y = sy/2 - 280, anchor = NW)
loginLabel.config(font = ("Courier", 44))
passwordLabel = Label(newAccountFrame, text = "Password: ", font = usernameFont, bg = accentColor)
passwordLabel.place(x = sx/2 - 155, y = sy/2 - 210, anchor = NW)
passwordConLabel = Label(newAccountFrame, text = "Confirm Password: ", font = usernameFont, bg = accentColor)
passwordConLabel.place(x = sx/2 - 155, y = sy/2 - 140, anchor = NW)

# Logo image
#logo = ImageTk.PhotoImage(Image.open("img/Dollar Sign.png").resize((120, 120)))
#logoImage = Label(image = logo)
#logoImage.place(x = sx/2, y = sy/2 - 270, anchor = N)


# Create input box for username and password
urInput = Entry(newAccountFrame, width = 20, font = inputFont)
urInput.place(x = sx/2, y = sy/2 - 250, anchor = N)
prInput = Entry(newAccountFrame, width = 20, font = inputFont, show = '*')
prInput.place(x=sx/2, y = sy/2 - 180, anchor = N)
pcInput = Entry(newAccountFrame, width = 20, font = inputFont, show = '*')
pcInput.place(x=sx/2, y = sy/2 - 110, anchor = N)


def registerAccount():
    print("Register account clicked")
    # Store entries
    userEntry = urInput.get()
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
                popupLogin("USER Exists already")
                foundFlag = True
    if not foundFlag:
        if passEntry != confEntry:
            popupLogin("Passwords don't match")
        else:
            with open ('UserData/userList.csv', 'a') as file:
                writer = csv.writer(file, lineterminator="\n")
                writer.writerow([userEntry, passEntry])
            print("User ", userEntry, "added!")
            popupLogin("USER ADDED")
            

    urInput.delete(0, END)
    prInput.delete(0, END)
    pcInput.delete(0, END)

#Create buttons
confirmButton = Button(newAccountFrame, text = "Register", bg = "#A9e451", padx = 10, pady = 0, font = ("Verdana", 15), command = registerAccount)
confirmButton.place(x = sx/2, y = sy/2 + 70, anchor = NW)
returnButton = Button(newAccountFrame, text = "Return to login", font = ("Verdana", 10), bg = mainColor, command = lambda: showFrame(loginFrame))
returnButton.place(x = sx/2 - 155, y = sy/2 + 80, anchor = NW)



loginFrame.mainloop()