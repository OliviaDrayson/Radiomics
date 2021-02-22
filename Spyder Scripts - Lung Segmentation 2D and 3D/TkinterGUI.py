#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 13:19:36 2021

@author: oliviadrayson
"""

#Tkinter GUI

import tkinter
import os

"""window = tkinter.Tk()

window.title("GUI")

# You will first create a division with the help of Frame class and align them on TOP and BOTTOM with pack() method.
top_frame = tkinter.Frame(window).pack()
bottom_frame = tkinter.Frame(window).pack(side = "bottom")

# Once the frames are created then you are all set to add widgets in both the frames.
btn1 = tkinter.Button(top_frame, text = "Button1", fg = "red").pack() #'fg or foreground' is for coloring the contents (buttons)

btn2 = tkinter.Button(top_frame, text = "Button2", fg = "green").pack()

btn3 = tkinter.Button(bottom_frame, text = "Button3", fg = "purple").pack(side = "left") #'side' is used to left or right align the widgets

btn4 = tkinter.Button(bottom_frame, text = "Button4", fg = "orange").pack(side = "left")

window.mainloop()

from tkinter import *
top = tkinter.Tk()
CheckVar1 = IntVar()
CheckVar2 = IntVar()
tkinter.Checkbutton(top, text = "Machine Learning",variable = CheckVar1,onvalue = 1, offvalue=0).grid(row=0,sticky=W)
tkinter.Checkbutton(top, text = "Deep Learning", variable = CheckVar2, onvalue = 0, offvalue =1).grid(row=1,sticky=W)
top.mainloop()

# Let's create the Tkinter window
window = tkinter.Tk()
window.title("GUI")

# creating a function called DataCamp_Tutorial()
def DataCamp_Tutorial():
    tkinter.Label(window, text = "GUI with Tkinter!").pack()

tkinter.Button(window, text = "Click Me!", command = DataCamp_Tutorial).pack()
window.mainloop()


# Let's create the Tkinter window
window = tkinter.Tk()

window.geometry("400x600")

window.title("GUI")

print(os.getcwd())

# In order to display the image in a GUI, you will use the 'PhotoImage' method of Tkinter. It will an image from the directory (specified path) and store the image in a variable.
icon = tkinter.PhotoImage(file = 'Telescope.png')

# Finally, to display the image you will make use of the 'Label' method and pass the 'image' variriable as a parameter and use the pack() method to display inside the GUI.
label = tkinter.Label(window, image = icon)
label.pack()

window.mainloop()"""

#CALCULATOR

from tkinter import *

# Let's create the Tkinter window
window = Tk()

# Then, you will define the size of the window in width(312) and height(324) using the 'geometry' method
window.geometry("500x350")

# In order to prevent the window from getting resized you will call 'resizable' method on the window
window.resizable(0, 0)

#Finally, define the title of the window
window.title("Calculator")


# Let's now define the required functions for the Calculator to function properly.

# 1. First is the button click 'btn_click' function which will continuously update the input field whenever a number is entered or any button is pressed it will act as a button click update.
def btn_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)

# 2. Second is the button clear 'btn_clear' function clears the input field or previous calculations using the button "C"
def btn_clear():
    global expression
    expression = ""
    input_text.set("")

# 3. Third and the final function is button equal ("=") 'btn_equal' function which will calculate the expression present in input field. For example: User clicks button 2, + and 3 then clicks "=" will result in an output 5.
def btn_equal():
    global expression
    result = str(eval(expression)) # 'eval' function is used for evaluating the string expressions directly
    # you can also implement your own function to evalute the expression istead of 'eval' function
    input_text.set(result)
    expression = ""

expression = ""
# In order to get the instance of the input field 'StringVar()' is used
input_text = StringVar()

# Once all the functions are defined then comes the main section where you will start defining the structure of the calculator inside the GUI.

# The first thing is to create a frame for the input field
input_frame = Frame(window, width = 312, height = 50, bd = 0, highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
input_frame.pack(side = TOP)


# Then you will create an input field inside the 'Frame' that was created in the previous step. Here the digits or the output will be displayed as 'right' aligned
input_field = Entry(input_frame, font = ('arial', 18, 'bold'), textvariable = input_text, width = 50, bg = "#eee", bd = 0, justify = RIGHT)
input_field.grid(row = 0, column = 0)
input_field.pack(ipady = 10) # 'ipady' is an internal padding to increase the height of input field


# Once you have the input field defined then you need a separate frame which will incorporate all the buttons inside it below the 'input field'
btns_frame = Frame(window, width = 312, height = 272.5, bg = "grey")
btns_frame.pack()


# The first row will comprise of the buttons 'Clear (C)' and 'Divide (/)'
clear = Button(btns_frame, text = "C", fg = "black", width = 32, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_clear()).grid(row = 0, column = 0, columnspan = 3, padx = 1, pady = 1)
divide = Button(btns_frame, text = "/", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("/")).grid(row = 0, column = 3, padx = 1, pady = 1)


# The second row will comprise of the buttons '7', '8', '9' and 'Multiply (*)'
seven = Button(btns_frame, text = "7", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(7)).grid(row = 1, column = 0, padx = 1, pady = 1)
eight = Button(btns_frame, text = "8", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(8)).grid(row = 1, column = 1, padx = 1, pady = 1)
nine = Button(btns_frame, text = "9", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(9)).grid(row = 1, column = 2, padx = 1, pady = 1)
multiply = Button(btns_frame, text = "*", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("*")).grid(row = 1, column = 3, padx = 1, pady = 1)


# The third row will comprise of the buttons '4', '5', '6' and 'Subtract (-)'
four = Button(btns_frame, text = "4", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(4)).grid(row = 2, column = 0, padx = 1, pady = 1)
five = Button(btns_frame, text = "5", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(5)).grid(row = 2, column = 1, padx = 1, pady = 1)
six = Button(btns_frame, text = "6", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(6)).grid(row = 2, column = 2, padx = 1, pady = 1)
minus = Button(btns_frame, text = "-", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("-")).grid(row = 2, column = 3, padx = 1, pady = 1)


# The fourth row will comprise of the buttons '1', '2', '3' and 'Addition (+)'
one = Button(btns_frame, text = "1", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(1)).grid(row = 3, column = 0, padx = 1, pady = 1)
two = Button(btns_frame, text = "2", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(2)).grid(row = 3, column = 1, padx = 1, pady = 1)
three = Button(btns_frame, text = "3", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(3)).grid(row = 3, column = 2, padx = 1, pady = 1)
plus = Button(btns_frame, text = "+", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("+")).grid(row = 3, column = 3, padx = 1, pady = 1)


# Finally, the fifth row will comprise of the buttons '0', 'Decimal (.)', and 'Equal To (=)'
zero = Button(btns_frame, text = "0", fg = "black", width = 21, height = 3, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(0)).grid(row = 4, column = 0, columnspan = 2, padx = 1, pady = 1)
point = Button(btns_frame, text = ".", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click(".")).grid(row = 4, column = 2, padx = 1, pady = 1)
equals = Button(btns_frame, text = "=", fg = "black", width = 10, height = 3, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_equal()).grid(row = 4, column = 3, padx = 1, pady = 1)


window.mainloop()


