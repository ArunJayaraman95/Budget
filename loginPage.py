# Imports
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
import csv

# Creating window
root=Tk()
  
# Set screen width (sx) and height (sy)
sx = root.winfo_screenwidth() 
sy = root.winfo_screenheight()

# Set the window size
root.geometry("%dx%d" % (sx, sy))
root.title("Budget Boi")
root.iconbitmap("img/WayneStateLogo.ico")

# Define colors
c1 = "#56C3A2"
c2 = "#41927A"

# Define fonts
buttonFont = font.Font(size = 24)
inputFont = font.Font(size = 20)

# Create canvas
canvas = Canvas(root, width = sx, height = sy)
canvas.pack()
canvas.config(background=c1)

# Form outline
canvas.create_rectangle(sx/2 - 200, sy/6, sx/2 + 200, 2*sy/3-50, fill = c2, width = 0)

# Create labels for login and place them
usernameFont = font.Font(size = 16)
usernameLabel = Label(root, text = "Username: ", font = usernameFont, bg = c2)
usernameLabel.place(x = sx/2 - 97, y = sy/2 - 100, anchor = N)
loginLabel = Label(root, text = "Login", font = usernameFont, bg = c2)
loginLabel.place(x = sx/2, y = sy/2 - 350, anchor = N)
loginLabel.config(font = ("Courier", 44))
passwordLabel = Label(root, text = "Password: ", font = usernameFont, bg = c2)
passwordLabel.place(x = sx/2 - 97, y = sy/2 - 20, anchor = N)

# Logo image
logo = ImageTk.PhotoImage(Image.open("img/Dollar Sign.png").resize((120, 120)))
logoImage = Label(image = logo)
logoImage.place(x = sx/2, y = sy/2 - 270, anchor = N)


# Create input box for username and password
uInput = Entry(root, width = 20, font = inputFont)
uInput.place(x = sx/2, y = sy/2 - 60, anchor = N)
pInput = Entry(root, width = 20, font = inputFont)
pInput.place(x=sx/2, y = sy/2 + 20, anchor = N)


activeUser = ""

def popupLogin(message):
    win = Toplevel()
    win.wm_title("Window")
    win.geometry("+%d+%d" % (sx/2 - 50, sy/2-200))
    l = Label(win, text=message)
    l.grid(row=0, column=0)

    b = Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)



def myClick():
    global activeUser
    print("Login submit button clicked")
    userEntry = uInput.get()
    passEntry = pInput.get()
    foundFlag = False
    # Check username
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
            warningLabel = Label(root, text = "Incorrent credentials", bg = c2)
            warningLabel.place(x = sx/2 - 30, y = sy/2 - 130, anchor = N)
    uInput.delete(0, END)

    print("Active user:", activeUser)


#Create button
submitButton = Button(root, text = "Submit", bg = "#A9e451", padx = 10, pady = 0, font = ("Verdana", 15), command = myClick)
submitButton.place(x = sx/2, y = sy/2 + 70, anchor = N)

root.mainloop()