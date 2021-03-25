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
from skimage.transform import rescale, resize
import numpy as np
 
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("CT Scan Analysis")
        
        #FRAMES
        
        self.MainFrame = tk.LabelFrame(master, width = 400, height = 660, relief='groove').grid(row=0, rowspan=14, column=0, columnspan=5)
        self.CanvasFrame = tk.LabelFrame(master, width = 660, height = 660, relief='groove').grid(row=0, rowspan=14, column=5, columnspan=5)
        
        self.prompt = StringVar()
        self.prompt.set("Image Name: ")
        self.date_text = StringVar()
        self.date_text.set("Image Date: ")
        self.slice = StringVar()
        self.slice.set("Slice: ")
        self.Area = StringVar()
        self.Area.set("Area (mm3) = ")
        self.Mean = StringVar()
        self.Mean.set("Mean (HU) = ")
        self.Median = StringVar()
        self.Median.set("Median (HU) = ")
        self.STD = StringVar()
        self.STD.set(str("Standard Deviation (HU) = "))
        
        #CANVAS
        self.canvas = tk.Canvas(self.CanvasFrame, bg ="white", width=640, height=640)
        self.canvas.grid(row=0, column=5, rowspan=14, columnspan=5)
        
        #MAIN FRAME
        self.openfile = tk.Button(self.MainFrame, text = "Choose Image Folder", command=self.OpenFile)
        self.openfile.grid(row=0,columnspan=5)
        
        self.label = tk.Label(self.MainFrame, textvariable=self.prompt) 
        self.label.grid(row=1,column=1, columnspan=4, sticky='W')
        
        self.date_label = tk.Label(self.MainFrame, textvariable=self.date_text)
        self.date_label.grid(row=2, column=1, columnspan=4, sticky='W')
        
        self.sliceL = tk.Label(self.MainFrame, textvariable = self.slice)
        self.sliceL.grid(row=3, rowspan=2 ,column=1, sticky='W')
        
        image = Image.open('DownArrow.png')
        down = image.resize((30, 30)) 
        up = down.rotate(180)
        
        self.UpArrow = ImageTk.PhotoImage(up)
        self.DownArrow = ImageTk.PhotoImage(down)
        
        self.button1 = tk.Button(self.MainFrame, text="Up", image=self.UpArrow, command=self.Up)
        self.button1.grid(row=3, column=2, columnspan=4, sticky='W')
        
        self.button2 = tk.Button(self.MainFrame, text="Down", image=self.DownArrow, command=self.Down)
        self.button2.grid(row=4, column=2, columnspan=4, sticky='W')
        
        self.button3 = tk.Button(self.MainFrame, text="Segment", command=self.Segment)
        self.button3.grid(row=5,columnspan=5)
        
        #EDITING SEGMENTATION
        self.dilate_button = tk.Button(self.MainFrame, text = "Dilate", command=self.dilate)
        self.dilate_button.grid(row=6,column=0, columnspan=3)
        
        self.erode_button = tk.Button(self.MainFrame, text = "Erode", command=self.erode)
        self.erode_button.grid(row=6,column=2, columnspan=2)
        
        self.fill_holes_button = tk.Button(self.MainFrame, text = "Fill Holes", command=self.fill_holes)
        self.fill_holes_button.grid(row=7,column=0, columnspan=3)
        
        self.revert = tk.Button(self.MainFrame, text = "Revert", command=self.Segment)
        self.revert.grid(row=7,column=2, columnspan=2)
        
        #STATISTICS
        self.labelA = tk.Label(master, textvariable=self.Area)
        self.labelA.grid(row=9,column=1,columnspan=4, sticky='W')
        
        self.labelM = tk.Label(master, textvariable=self.Mean)
        self.labelM.grid(row=10,column=1, columnspan=4, sticky='W')
        
        self.labelMed = tk.Label(master, textvariable=self.Median)
        self.labelMed.grid(row=11,column=1, columnspan=4, sticky='W')
        
        self.labelSTD = tk.Label(master, textvariable=self.STD)
        self.labelSTD.grid(row=12,column=1, columnspan=4, sticky='W')
        
        #SAVE TO EXCEL
        self.excel = tk.Button(master, text = "Save to Excel", command=self.SaveData)
        self.excel.grid(row=13,columnspan=5)
        
        self.saved = StringVar()
        self.saved.set("")
        self.Saved = tk.Label(master,textvariable=self.saved)
        self.Saved.grid(row=14,columnspan=5)
        
        self.pressed = 0
        self.enabled = 0
        self.dilate_pressed = 0
        self.erode_pressed = 0
        self.fill_pressed = 0
        
        if self.enabled == 0:
            self.button1["state"] = "disabled"
            self.button2["state"] = "disabled"
            self.button3["state"] = "disabled"
            self.excel["state"] = "disabled"
            
            self.dilate_button["state"] = "disabled"
            self.erode_button["state"] = "disabled"
            self.fill_holes_button["state"] = "disabled"
            self.revert["state"] = "disabled"
        
        self.Chosen = 100
        
    def OpenFile(self):
        self.directory = fd.askdirectory()
        IMG3D, StudyDate, MouseName, ps, ss = fs.DICOM(self.directory)
        text = "Image Name: " + str(MouseName)
        self.prompt.set(str(text))
        date = "Image Date: " + str(StudyDate[0:4]) + "/" + str(StudyDate[4:6]) + "/" + str(StudyDate[6:8])
        self.date_text.set(date)
        
        self.Date = StudyDate
        self.IMAGE = IMG3D

        if self.enabled == 0:
            self.Chosen = fs.SliceChoice(self.IMAGE)
        
        IMAGE = fs.GetImage(self.IMAGE, self.Chosen)

        #RESCALING IMAGE
        x_factor = 640/IMAGE.shape[0]
        y_factor = 640/IMAGE.shape[1]
        
        if x_factor < y_factor:
            IMAGE = rescale(IMAGE, x_factor, anti_aliasing=False)
        else:
            IMAGE = rescale(IMAGE, y_factor, anti_aliasing=False)
        
        Width, Height = IMAGE.shape
        x_start = int(round((640 - Width)/2))
        y_start = int(round((640 - Height)/2))
        IMAGE = fs.convert(IMAGE, 0, 255, np.uint8)

        im = Image.fromarray(IMAGE) #Pillow
        self.shape = IMAGE.shape
        
        self.img = ImageTk.PhotoImage(image=im)
        self.image_on_canvas = self.canvas.create_image(y_start, x_start, anchor=tk.NW, image=self.img)
        
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
        
       #RESCALING IMAGE
        x_factor = 640/IMAGE.shape[0]
        y_factor = 640/IMAGE.shape[1]
        
        if x_factor < y_factor:
            IMAGE = rescale(IMAGE, x_factor, anti_aliasing=False)
        else:
            IMAGE = rescale(IMAGE, y_factor, anti_aliasing=False)
        
        Width, Height = IMAGE.shape
        x_start = int(round((640 - Width)/2))
        y_start = int(round((640 - Height)/2))
        IMAGE = fs.convert(IMAGE, 0, 255, np.uint8)

        im = Image.fromarray(IMAGE) #Pillow
        
        self.img = ImageTk.PhotoImage(image=im)
        self.image_on_canvas = self.canvas.create_image(y_start, x_start, anchor=tk.NW, image=self.img)
        
        text = str("Slice: " + str(slice_no))
        self.slice.set(text)
        
    def Down(self):
        self.pressed -= 1
        slice_no = self.pressed + self.Chosen
        IMAGE = fs.GetImage(self.IMAGE, slice_no)
        
        #RESCALING IMAGE
        x_factor = 640/IMAGE.shape[0]
        y_factor = 640/IMAGE.shape[1]
        
        if x_factor < y_factor:
            IMAGE = rescale(IMAGE, x_factor, anti_aliasing=False)
        else:
            IMAGE = rescale(IMAGE, y_factor, anti_aliasing=False)
        
        Width, Height = IMAGE.shape
        x_start = int(round((640 - Width)/2))
        y_start = int(round((640 - Height)/2))
        IMAGE = fs.convert(IMAGE, 0, 255, np.uint8)

        im = Image.fromarray(IMAGE) #Pillow
        
        self.img = ImageTk.PhotoImage(image=im)
        self.image_on_canvas = self.canvas.create_image(y_start, x_start, anchor=tk.NW, image=self.img)
                
        text = str("Slice: " + str(slice_no))
        self.slice.set(text)
    
    def Segment(self):
        
        self.dilate_pressed = 0
        self.erode_pressed = 0
        self.fill_pressed = 0
        
        self.slice_no = self.pressed + self.Chosen
        IMAGE_S, mmArea1, mmArea2, mean, median, std = fs.SliceSegment(self.IMAGE, self.slice_no, ps, ss)
 
        self.mmArea2 = round(mmArea2,2)
        self.mean = round(mean,2)
        self.median = round(median,2)
        self.std = round(std,2)
        
        #RESIZING IMAGE
        x, y = self.shape
        IMAGE_S = resize(IMAGE_S, (x, y, 3))
        IMAGE_S = fs.convert(IMAGE_S, 0, 255, np.uint8)

        self.img = ImageTk.PhotoImage(image=Image.fromarray(IMAGE_S))
        self.canvas.itemconfig(self.image_on_canvas, image = self.img)

        self.Area.set(str("Area (mm3) = " + str(self.mmArea2)))
        self.Mean.set(str("Mean (HU) = " + str(self.mean)))
        self.Median.set(str("Median (HU) = " + str(self.median)))
        self.STD.set(str("Standard Deviation (HU) = " + str(self.std)))
        
        self.excel["state"] = "normal"
        self.dilate_button["state"] = "normal"
        self.erode_button["state"] = "normal"
        self.fill_holes_button["state"] = "normal"
        self.revert["state"] = "normal"
        self.saved.set("")
        
    def dilate(self):
        
        self.dilate_pressed = self.dilate_pressed + 1
        
        self.slice_no = self.pressed + self.Chosen
        IMAGE_S, mmArea1, mmArea2, mean, median, std = fs.SliceSegment(self.IMAGE, self.slice_no, ps, ss, d=self.dilate_pressed, e=self.erode_pressed, f=self.fill_pressed)
        
        self.mmArea2 = round(mmArea2,2)
        self.mean = round(mean,2)
        self.median = round(median,2)
        self.std = round(std,2)
        
        #RESIZING IMAGE
        x, y = self.shape
        IMAGE_S = resize(IMAGE_S, (x, y, 3))
        IMAGE_S = fs.convert(IMAGE_S, 0, 255, np.uint8)

        self.img = ImageTk.PhotoImage(image=Image.fromarray(IMAGE_S))
        self.canvas.itemconfig(self.image_on_canvas, image = self.img)

        self.Area.set(str("Area (mm3) = " + str(self.mmArea2)))
        self.Mean.set(str("Mean (HU) = " + str(self.mean)))
        self.Median.set(str("Median (HU) = " + str(self.median)))
        self.STD.set(str("Standard Deviation (HU) = " + str(self.std)))
        
        self.excel["state"] = "normal"
        self.dilate_button["state"] = "normal"
        self.erode_button["state"] = "normal"
        self.fill_holes_button["state"] = "normal"
        self.saved.set("")
        
    def erode(self):
        
        self.erode_pressed = self.erode_pressed + 1
        
        self.slice_no = self.pressed + self.Chosen
        IMAGE_S, mmArea1, mmArea2, mean, median, std = fs.SliceSegment(self.IMAGE, self.slice_no, ps, ss, d=self.dilate_pressed, e=self.erode_pressed, f=self.fill_pressed)
        
        self.mmArea2 = round(mmArea2,2)
        self.mean = round(mean,2)
        self.median = round(median,2)
        self.std = round(std,2)
        
        #RESIZING IMAGE
        x, y = self.shape
        IMAGE_S = resize(IMAGE_S, (x, y, 3))
        IMAGE_S = fs.convert(IMAGE_S, 0, 255, np.uint8)

        self.img = ImageTk.PhotoImage(image=Image.fromarray(IMAGE_S))
        self.canvas.itemconfig(self.image_on_canvas, image = self.img)

        self.Area.set(str("Area (mm3) = " + str(self.mmArea2)))
        self.Mean.set(str("Mean (HU) = " + str(self.mean)))
        self.Median.set(str("Median (HU) = " + str(self.median)))
        self.STD.set(str("Standard Deviation (HU) = " + str(self.std)))
        
        self.excel["state"] = "normal"
        self.dilate_button["state"] = "normal"
        self.erode_button["state"] = "normal"
        self.fill_holes_button["state"] = "normal"
        self.saved.set("")
        
    def fill_holes(self):
        
        self.fill_pressed = self.fill_pressed + 1
        
        self.slice_no = self.pressed + self.Chosen
        IMAGE_S, mmArea1, mmArea2, mean, median, std = fs.SliceSegment(self.IMAGE, self.slice_no, ps, ss, d=self.dilate_pressed, e=self.erode_pressed, f=self.fill_pressed)

        self.mmArea2 = round(mmArea2,2)
        self.mean = round(mean,2)
        self.median = round(median,2)
        self.std = round(std,2)
        
        #RESIZING IMAGE
        x, y = self.shape
        IMAGE_S = resize(IMAGE_S, (x, y, 3))
        IMAGE_S = fs.convert(IMAGE_S, 0, 255, np.uint8)

        self.img = ImageTk.PhotoImage(image=Image.fromarray(IMAGE_S))
        self.canvas.itemconfig(self.image_on_canvas, image = self.img)

        self.Area.set(str("Area (mm3) = " + str(self.mmArea2)))
        self.Mean.set(str("Mean (HU) = " + str(self.mean)))
        self.Median.set(str("Median (HU) = " + str(self.median)))
        self.STD.set(str("Standard Deviation (HU) = " + str(self.std)))
        
        self.excel["state"] = "normal"
        self.dilate_button["state"] = "normal"
        self.erode_button["state"] = "normal"
        self.fill_holes_button["state"] = "normal"
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
