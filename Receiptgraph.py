import tkinter as tk
from tkinter.constants import *
from tkinter import Listbox, PhotoImage, Scrollbar, Widget, ttk
from tkinter import simpledialog
from tkinter.filedialog import askopenfile
from typing import Sized
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from PIL import Image, ImageTk


LARGEFONT =("Verdana", 35)
reciepts = {}

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage, Page1, Page2):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		# label of frame Layout 2
		label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
		
		# putting the grid in its place by using
		# grid
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		button1 = ttk.Button(self, text ="Receipt Vault",
		command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		## button to show frame 2 with text layout2
		button2 = ttk.Button(self, text ="Spedning Graph",
		command = lambda : controller.show_frame(Page2))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		


# second window frame page1
class Page1(tk.Frame):

	def recieptBook(self):
		# This is where users can scroll through past receipts
		recieptViewer = tk.Toplevel(app)
		recieptViewer.title("Wallet")
		recieptViewer.geometry('400x300')

		recieptsList = Listbox(recieptViewer)
		recieptsList.pack(side = LEFT, fill = BOTH, expand=True)
		scroll = Scrollbar(recieptViewer)
		scroll.pack(side= RIGHT, fill=BOTH)
		recieptsList.config(yscrollcommand=scroll.set)
		scroll.config(command=recieptsList.yview)

		for i in reciepts:
			recieptsList.insert(END, i)

		recieptsList.bind('<<ListboxSelect>>', self.CurSelect)

	# helper function for upload
	def open_file(self):
		file_path = askopenfile(mode='r', filetypes=[('Image Files', '*jpg')])
		if file_path is not None:
			exp = simpledialog.askinteger(title="Expense Report", prompt="Total Expense for Receipt")
			reciepts[file_path.name] = exp
			pass
	
	def CurSelect(self, event):

		widget = event.widget
		selection= widget.curselection()
		picked = widget.get(selection[0])
		loaded = Image.open(picked)
		loaded = loaded.resize((400,400))
		render = ImageTk.PhotoImage(loaded)
		
		imageShow = tk.Toplevel(app)
		imageShow.title(reciepts[picked])
		imageShow.geometry('400x400')
		img = ttk.Label(imageShow, image=render)
		img.image = render
		img.place(x=0,y=0)
		print(picked)

	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Receipt Vault", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="StartPage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button2 = ttk.Button(self, text ="Spending Graph",
							command = lambda : controller.show_frame(Page2))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)


		#This is the button for inputting receipt
		image_input = ttk.Button(self, text="Input Receipt", command= lambda : self.open_file())
		image_input.grid(row = 1, column=5)

		#This is the button for viewing receipt
		image_input = ttk.Button(self, text="Show Wallet", command= lambda : self.recieptBook())
		image_input.grid(row = 2, column=5)




# third window frame page2
class Page2(tk.Frame):

	# refresh the frame
	def refresh(self, parent, controller):
		plot.tight_layout()
		# This is where the plot is generated
		fig = Figure(figsize=(4,3), dpi=80)
		x = []
		for i in range(1,len(reciepts)+1):
			x.append(i)
		plt= fig.add_subplot(111)
		plt.plot(x, reciepts.values())
		plt.autoscale()
		plt.set_xticks(x)
		plt.set_xlabel("Receipt Number")
		plt.set_ylabel("Amount ($)")
		
		canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
		canvas.draw()
		canvas.get_tk_widget().grid(row=2, column= 4, ipadx = 60, ipady = 60,)

		toolbar = tk.Frame(self)
		toolbar.update()
		canvas.get_tk_widget().grid(row=2, column= 4, ipadx = 60, ipady = 60)

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Spending Graph", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="Receipt Vault",
							command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 3 with text
		# layout3
		button2 = ttk.Button(self, text ="Startpage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		print("rendering ploit page")

		# button to REFRESH
		refresh_button = ttk.Button(self, text ="Refresh",
							command = lambda : self.refresh(parent, controller))
	
		# putting the button in its place by
		# using grid
		refresh_button.grid(row = 1, column = 4, padx = 10, pady = 10)



# Driver Code
app = tkinterApp()
app.geometry('800x500')
app.mainloop()
