# -*- coding: utf-8 -*-
"""
Main Graphical User Interface Code

@author: oliviadrayson
"""

#Using Tkinter to make a GUI
#!pip install pandas


import FunctionsScript as fs

#-------------------------------

# Create DICOM image for the folder name
img3dR, StudyDate, MouseName, ps, ss = fs.DICOM('604')

Year = StudyDate[0:4]
Month = StudyDate[4:6]
Day = StudyDate[6:8]

IMAGE = fs.GetImage(img3dR, 100) # Normalise image for viewing

#---- LOADING IMAGE

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter import StringVar
import pandas as pd
global pressed
 
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("CT Scan Analysis")
        
        self.prompt = StringVar()
        self.prompt.set("CT Scan Analysis Program")
        self.slice = StringVar()
        self.slice.set("")
        self.Area = StringVar()
        self.Area.set("Area (mm3) = ")
        self.Mean = StringVar()
        self.Mean.set("Mean (HU) = ")
        self.Median = StringVar()
        self.Median.set("Median (HU) = ")
        self.STD = StringVar()
        self.STD.set(str("Standard Deviation (HU) = "))
        
        self.openfile = tk.Button(master, text = "Choose Directory", command=self.OpenFile)
        self.openfile.grid(row=0,columnspan=3)
        
        self.sliceL = tk.Label(master, textvariable = self.slice)
        self.sliceL.grid(row=0,column=3,columnspan=3)
        
        self.canvas = tk.Canvas(self.master, bg ="blue", width=350, height=350)
        self.canvas.grid(row=1,columnspan=6)
        
        self.label = tk.Label(master, textvariable=self.prompt)
        self.label.grid(row=2,columnspan=6)
        
        self.im = tk.Button(master, text="Generate Image", command = self.GenerateImage)
        self.im.grid(row=3,columnspan=6)
                
        self.button1 = tk.Button(master, text="<=", command=self.Up)
        self.button1.grid(row=4,column=2)
        
        self.button2 = tk.Button(master, text="=>", command=self.Down)
        self.button2.grid(row=4,column=3)
        
        self.button3 = tk.Button(master, text="Segment", command=self.Segment)
        self.button3.grid(row=5,columnspan=6)
        
        #EMPTY LABELS FOR GRID
        
        self.label0 = tk.Label(master, text=" ")
        self.label0.grid(row=4,column=0)
        
        self.label1 = tk.Label(master, text=" ")
        self.label1.grid(row=4,column=1)
        
        self.label2 = tk.Label(master, text=" ")
        self.label2.grid(row=4,column=4)
        
        self.label4 = tk.Label(master, text=" ")
        self.label4.grid(row=4,column=5)
        
        #STATISTICS
        self.labelA = tk.Label(master, textvariable=self.Area)
        self.labelA.grid(row=6,columnspan=6)
        
        self.labelM = tk.Label(master, textvariable=self.Mean)
        self.labelM.grid(row=7,columnspan=6)
        
        self.labelMed = tk.Label(master, textvariable=self.Median)
        self.labelMed.grid(row=8,columnspan=6)
        
        self.labelSTD = tk.Label(master, textvariable=self.STD)
        self.labelSTD.grid(row=9,columnspan=6)
        
        #SAVE TO EXCEL
        self.excel = tk.Button(master, text = "Save to Excel", command=self.SaveData)
        self.excel.grid(row=10,columnspan=6)
        
        self.saved = StringVar()
        self.saved.set("")
        self.Saved = tk.Label(master,textvariable=self.saved)
        self.Saved.grid(row=11,columnspan=6)
        
        self.pressed = 0
        self.enabled = 0
        
        if self.enabled == 0:
            self.button1["state"] = "disabled"
            self.button2["state"] = "disabled"
            self.im["state"] = "disabled"
            self.button3["state"] = "disabled"
            self.excel["state"] = "disabled"
        
        self.Chosen = 100
        
    def OpenFile(self):
        self.directory = fd.askdirectory()
        IMG3D, StudyDate, MouseName, ps, ss = fs.DICOM(self.directory)
        self.im["state"] = "normal"
        text = str(MouseName) + ": " + str(StudyDate[0:4]) + "/" + str(StudyDate[4:6]) + "/" + str(StudyDate[6:8])
        self.prompt.set(str(text))
        self.Date = StudyDate
        self.IMAGE = IMG3D
        
    def GenerateImage(self):
        
        if self.enabled == 0:
            self.Chosen = fs.SliceChoice(self.IMAGE)
        
        IMAGE = fs.GetImage(self.IMAGE, self.Chosen)

        self.img = ImageTk.PhotoImage(image=Image.fromarray(IMAGE))
        self.image_on_canvas = self.canvas.create_image(25, 25, anchor=tk.NW, image=self.img)
        self.pressed=0
        self.enabled=1
        
        self.button1["state"] = "normal"
        self.button2["state"] = "normal"
        self.button3["state"] = "normal"
        
        text = str("Slice: " + str(self.Chosen + self.pressed))
        self.slice.set(text)
        
    def Up(self):
        self.pressed += 1
        slice_no = self.pressed + self.Chosen
        IMAGE = fs.GetImage(self.IMAGE, slice_no)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(IMAGE))
        self.canvas.itemconfig(self.image_on_canvas, image = self.img)
        
        text = str("Slice: " + str(slice_no))
        self.slice.set(text)
        
    def Down(self):
        self.pressed -= 1
        slice_no = self.pressed + self.Chosen
        IMAGE = fs.GetImage(self.IMAGE, slice_no)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(IMAGE))
        self.canvas.itemconfig(self.image_on_canvas, image = self.img)
        
        text = str("Slice: " + str(slice_no))
        self.slice.set(text)
    
    def Segment(self):
        self.slice_no = self.pressed + self.Chosen
        IMAGE_S, mmArea1, mmArea2, mean, median, std = fs.SliceSegment(self.IMAGE, self.slice_no, ps, ss)
        
        self.mmArea2 = round(mmArea2,2)
        self.mean = round(mean,2)
        self.median = round(median,2)
        self.std = round(std,2)
        
        self.img = ImageTk.PhotoImage(image=Image.fromarray(IMAGE_S))
        self.canvas.itemconfig(self.image_on_canvas, image = self.img)
        self.Area.set(str("Area (mm3) = " + str(self.mmArea2)))
        self.Mean.set(str("Mean (HU) = " + str(self.mean)))
        self.Median.set(str("Median (HU) = " + str(self.median)))
        self.STD.set(str("Standard Deviation (HU) = " + str(self.std)))
        
        self.excel["state"] = "normal"
        self.saved.set("")
        
    def SaveData(self):
        
        d = {'ID': [604], 'Scan Date': [self.Date], 'Slice no': [self.slice_no], 'Mean (HU)': [self.mean], 'Median (HU)': [self.median],'Standard Deviation':[self.std],'Area (mm3)': [self.mmArea2]}
        df = pd.DataFrame(data=d)
        
        file = 'CBCT_OUT_DATA.xlsx'
        writer = pd.ExcelWriter(file, engine='xlsxwriter')
        df.to_excel(writer, 'Sheet1', index = False)
        writer.save()
        
        self.saved.set(str("Saved to Excel file: " + str(file)))
        
        
        
 
master = tk.Tk()

app = Application(master=master)

app.mainloop()
