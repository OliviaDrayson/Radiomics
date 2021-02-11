#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:53:05 2021

@author: oliviadrayson
"""

import FeatureExtraction as fe

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter import StringVar, IntVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from skimage.transform import rescale
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure

import SimpleITK as sitk
import math
import glob

import os
import openpyxl

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("3D Segmentation and Feature Extraction")
        
        self.Quit = tk.Button(master, text="QUIT", command=self.QUIT).grid(row=23, column=9, sticky='E')
        self.Name = tk.Label(master, text="Made by @OliviaDrayson : email drayson.o@mac.com").grid(row=23,column=8, sticky='E')
        
        self.canvas = tk.Canvas(self.master, bg ="white", width=650, height=650)
        self.canvas.grid(row = 0, column = 4, rowspan=23, columnspan=6)
        
        self.BatchLabel = tk.Label(master, text = "----- Batch Mode -----").grid(row=0,columnspan=4)
        
        self.Batch = tk.Button(master, text="Choose Images Folder", command=self.BatchMode)
        self.Batch.grid(row=1,columnspan=4)
        
        self.IndividualLabel = tk.Label(master, text = "----- Single Mode -----").grid(row=2,columnspan=4)
        
        self.openfile = tk.Button(master, text = "Choose Image Directory", command=self.OpenFile)
        self.openfile.grid(row = 3,columnspan=4)
        
        self.prompt = StringVar()
        self.prompt.set("Name:")
        
        self.prompt2 = StringVar()
        self.prompt2.set("Date:")
        
        self.label = tk.Label(master, textvariable=self.prompt)
        self.label.grid(row = 4, column=0, columnspan=4, sticky='W')
        
        self.label2 = tk.Label(master, textvariable=self.prompt2)
        self.label2.grid(row = 5, column=0, columnspan=4, sticky='W')
        
        self.segment = tk.Button(master, text ="3D Segmentation", command=self.Segment)
        self.segment.grid(row=6, column=0, columnspan=2)
        
        self.View = tk.Button(master, text = "3D View", command=self.Viewer)
        self.View.grid(row=6,column=2, columnspan=2)
        
        self.LabelFE = tk.Label(master, text = "Radiomic Feature Customisation:")
        self.LabelFE.grid(row=7,column=0, columnspan=4)
        
        #Feature Extraction Section
        
        self.firstorder = IntVar()
        self.firstorder.set(1)
        self.FirstOrder = tk.Checkbutton(master, text = "First Order", variable=self.firstorder)
        self.FirstOrder.grid(row=8, column=0,columnspan=2, sticky='W')
        
        self.glcm = IntVar()
        self.glcm.set(1)
        self.Glcm = tk.Checkbutton(master, text = "GLCM", variable=self.glcm)
        self.Glcm.grid(row=8, column=2,columnspan=2, sticky='W')
        
        self.shape = IntVar()
        self.shape.set(1)
        self.Shape = tk.Checkbutton(master, text = "Shape", variable=self.shape)
        self.Shape.grid(row=9, column=0, columnspan=2, sticky='W')
        
        self.glrlm = IntVar()
        self.glrlm.set(1)
        self.Glrlm = tk.Checkbutton(master, text = "GLRLM", variable=self.glrlm)
        self.Glrlm.grid(row=9, column=2, columnspan=2, sticky='W')
        
        self.glszm = IntVar()
        self.glszm.set(1)
        self.Glszm = tk.Checkbutton(master, text = "GLSZM", variable=self.glszm)
        self.Glszm.grid(row=10, column=0, columnspan=2, sticky='W')
        
        self.wavelet = IntVar()
        self.wavelet.set(1)
        self.Wavelet = tk.Checkbutton(master, text = "Wavelet Filtering", variable=self.wavelet)
        self.Wavelet.grid(row=10, column=2, columnspan=2, sticky='W')
        
        self.Estimate = tk.Button(master, text = "Estimate extraction time", command = self.Estimation)
        self.Estimate.grid(row=11, column=0, columnspan=2, sticky = 'W')
        
        self.time = StringVar()
        self.time.set("- mins -- secs")
        self.Time = tk.Label(master, textvariable = self.time).grid(row=11, column=2, columnspan=2, sticky = 'W')
        
        self.FeatureE = tk.Button(master, text = "Feature Extraction", command=self.FeatureExtract)
        self.FeatureE.grid(row=12,column=0, columnspan=4)
        
        self.OutputLabel = tk.Label(master, text="----- Output -----").grid(row=13,columnspan=4)
        
        self.OutputDirectory = tk.Button(master, text = "Choose Output Directory", command=self.OutputFolder)
        self.OutputDirectory.grid(row=14, columnspan=4)
        
        self.OUT = tk.Button(master, text = "Choose Output File", command = self.OutputFile)
        self.OUT.grid(row=15, columnspan=4)
        
        self.Single = tk.Label(master, text="Single Mode Only:").grid(row=16,columnspan=4)
        
        self.make_excel = IntVar()
        self.Make_Excel = tk.Checkbutton(master, text = "Create New Excel File", variable=self.make_excel)
        self.Make_Excel.grid(row=17, sticky='W')
        
        self.add_excel = IntVar()
        self.Add_Excel = tk.Checkbutton(master, text = "Add to Existing Excel File", variable=self.add_excel)
        self.Add_Excel.grid(row=18, sticky='W')
        
        self.Batch = tk.Label(master, text="Batch Mode Only:").grid(row=19,columnspan=4)
        
        self.many_excel = IntVar()
        self.Many_Excel = tk.Checkbutton(master, text = "Create File For Each Segmentation", variable=self.many_excel)
        self.Many_Excel.grid(row=20, sticky='W')
        
        self.one_excel = IntVar()
        self.One_Excel = tk.Checkbutton(master, text = "Create One Combined File", variable=self.one_excel)
        self.One_Excel.grid(row=21, sticky='W')
    
        self.loading = StringVar()
        self.loading.set("")
        self.Loading = tk.Label(master, textvariable = self.loading).grid(row=22,columnspan=4)
        
        #Disable inactive buttons
        self.activated = 0
        
        self.out_directory = 'a'
        self.excel_file = 'a'
        
        if self.activated == 0:
            self.segment["state"] = "disabled"
            self.View["state"] = "disabled"
            self.FeatureE["state"] = "disabled"
        
    def OpenFile(self):
        self.directory = fd.askdirectory()
        self.IMG3D, StudyDate, MouseName, ps, ss = fe.DICOM(self.directory)
        text = "Name: " + str(MouseName)
        text2 = "Date: " + str(StudyDate[0:4]) + "/" + str(StudyDate[4:6]) + "/" + str(StudyDate[6:8])
        self.prompt.set(str(text))
        self.prompt2.set(str(text2))
    
        self.Chosen = fe.SliceChoice(self.IMG3D)
        IMAGE = fe.GetImage(self.IMG3D, self.Chosen)

        #RESCALING IMAGE
        x_factor = 650/IMAGE.shape[0]
        y_factor = 650/IMAGE.shape[1]
        
        if x_factor < y_factor:
            IMAGE = rescale(IMAGE, x_factor, anti_aliasing=False)
        else:
            IMAGE = rescale(IMAGE, y_factor, anti_aliasing=False)
        
        Width, Height = IMAGE.shape
        x_start = int(round((650 - Width)/2))
        y_start = int(round((650 - Height)/2))
        IMAGE = fe.convert(IMAGE, 0, 255, np.uint8)

        im = Image.fromarray(IMAGE) #Pillow
        
        self.img = ImageTk.PhotoImage(image=im)
        self.image_on_canvas = self.canvas.create_image(y_start, x_start, anchor=tk.NW, image=self.img)
        
        self.segment["state"] = "normal"
        self.activated = 1
        self.Name = MouseName
        self.Date = StudyDate
            
    def Segment(self):
        
        self.Mask = fe.Segment4(self.IMG3D) #outputs mask
        Segmentation = self.Mask * self.IMG3D #convert from binary to real image
        
        IMAGE = fe.GetImage(Segmentation, self.Chosen)
        
        #RESCALING IMAGE
        x_factor = 650/IMAGE.shape[0]
        y_factor = 650/IMAGE.shape[1]
        
        if x_factor < y_factor:
            IMAGE = rescale(IMAGE, x_factor, anti_aliasing=False)
        else:
            IMAGE = rescale(IMAGE, y_factor, anti_aliasing=False)
        
        Width, Height = IMAGE.shape
        self.x_start = int(round((650 - Width)/2))
        self.y_start = int(round((650 - Height)/2))
        IMAGE = fe.convert(IMAGE, 0, 255, np.uint8)

        im = Image.fromarray(IMAGE) #Pillow
                
        self.img = ImageTk.PhotoImage(image=im)
        self.image_on_canvas = self.canvas.create_image(self.y_start, self.x_start, anchor=tk.NW, image=self.img)
    
        self.View["state"] = "normal"
        self.FeatureE["state"] = "normal"
    
    def Viewer(self):
        mesh = fe.MeshGeneration(self.Mask)     
        
        figure = Figure(figsize=(9, 9))
        ax= figure.add_subplot(1, 1, 1, projection='3d')

        ax.add_collection3d(mesh)
        
        p = self.Mask

        ax.set_xlim(0, p.shape[0])
        ax.set_ylim(0, p.shape[0])
        ax.set_zlim(0, p.shape[0])
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        self.Canvas = FigureCanvasTkAgg(figure, self.master)
        
        self.Canvas.get_tk_widget().grid(row=0,column=4,rowspan=23, columnspan=6)
        
        self.Canvas.mpl_connect('button_press_event', ax._button_press)
        self.Canvas.mpl_connect('button_release_event', ax._button_release)
        self.Canvas.mpl_connect('motion_notify_event', ax._on_move)
        
    def Estimation(self):
        
        if self.wavelet.get() == 1:
            if self.firstorder.get() * self.glcm.get() * self.shape.get() * self.glrlm.get() * self.glszm.get() == 1:
                time = 200
            else:
                time = 18*self.firstorder.get() + 35*self.glcm.get() + 135*self.shape.get() + 60*self.glrlm.get() + 35*self.glszm.get()
        else:
            if self.firstorder.get() * self.glcm.get() * self.shape.get() * self.glrlm.get() * self.glszm.get() == 1:
                time = 65
            else:
                time = 5*self.firstorder.get() + 5*self.glcm.get() + 60*self.shape.get() + 5*self.glrlm.get() + 5*self.glszm.get()
        
        minutes = math.floor(time/60)
        seconds = time - 60*minutes
        
        time_txt = str(minutes) + " mins " + str(seconds) + " secs"
        
        self.time.set(time_txt)
        
    def FeatureExtract(self):
        
        print("--STARTING SINGLE RUN--")
        
        print("Calculating Features...")
    
        self.Mask = self.Mask.astype(int)
        
        Image = sitk.GetImageFromArray(self.IMG3D)
        Mask = sitk.GetImageFromArray(self.Mask)
        
        #CHECK BOX
        CHECK_BOX = [self.firstorder.get(), self.glcm.get(), self.shape.get(), self.glrlm.get(), self.glszm.get(), self.wavelet.get()]
        
        FeatureVector, df = fe.Radiomics(Image, Mask, CHECK_BOX)
        
        if self.make_excel.get() == 1:        
            if self.out_directory == 'a':
            
                file = "output.xlsx"
                df.to_excel(file)  
                
                print("Saved to directory: " + os.getcwd())
        
            else:
                
                file = "output.xlsx"
                filepath = os.path.join(self.out_directory, file)
                
                df.to_excel(filepath)
                
                print("Saved to directory: " + self.out_directory)
            
        
            self.loading.set('Run Complete! Saved as: ' + file)

        if self.add_excel.get() == 1:
            
            if self.excel_file == 'a':
                
                print('Please select file to append data to')
                self.loading.set('Please select file to append data to and try again')
            
            else:   
            
                print('Adding to existing excel file')
                
                #old_df = pd.read_excel(self.excel_file, index_col=0) 
                old_df = openpyxl.load_workbook(self.excel_file)
                
                old_df = old_df['Sheet1']
                
                data = old_df.values
                columns = next(data)[0:]
                
                old_df = pd.DataFrame(data,columns=columns)
                
                old_df.drop(old_df.columns[[0]], axis=1, inplace=True)
                
                ID = self.Name                
                
                new_file = fe.ExcelFile(df, old_df, ID, self.Date)
                
                new_file.to_excel(self.excel_file) 
    
        print('--END OF SINGLE RUN--')
    
    def BatchMode(self):
        
        print("--STARTING BATCH RUN--")
        
        bdirectory = fd.askdirectory()
        bdir = str(bdirectory) + "/*"
        bdir2 = str(bdirectory) + "/"
        
        if self.out_directory == 'a': #if output directory is not defined
            self.out_directory = bdirectory
        
        counter = 0
        
        folders = glob.glob(bdir)
        
        for folder in folders:
        
            folder_name = folder.replace(bdir2, '')
            print("Now Segmenting: " + folder_name)
            
            IMAGE, StudyDate, MouseName, ps, ss = fe.DICOM(folder)
            
            Mask = fe.Segment4(IMAGE) #outputs mask
            
            fe.Viewer(Mask, folder_name)
                
            print("Calculating Features for: " + folder_name)
    
            Mask = Mask.astype(int)
        
            Image = sitk.GetImageFromArray(IMAGE)
            Mask = sitk.GetImageFromArray(Mask)
        
            #CHECK BOX
            CHECK_BOX = [self.firstorder.get(), self.glcm.get(), self.shape.get(), self.glrlm.get(), self.glszm.get(), self.wavelet.get()]
            
            FeatureVector, df = fe.Radiomics(Image, Mask, CHECK_BOX)
            
            if self.many_excel.get() == 1:
                
                file = str(folder_name + StudyDate + "_output.xlsx")
                df.to_excel(file)
                print("Features have been saved to " + file + "\n")
                   
            if self.one_excel.get() == 1:
                if counter == 0:
                    
                    ID = ['Image ID', 'Study Date']
                    Features = df["Feature"].values.tolist()
                    
                    Features = ID + Features
                    features = []
            
                    for feature in Features:
                        if 'diagnostics' not in feature:
                            features.append(feature)
                    
                    Data_Frame = pd.DataFrame(columns = features)
            
                Data_Frame = fe.ExcelFile(df, Data_Frame, folder_name, StudyDate) #adding output data to massive data file 
            
            
            counter += 1

        if self.one_excel.get() == 1:
            
            one_file = "Extraction_Output.xlsx"
            
            if self.out_directory != 0:
                one_file = os.path.join(self.out_directory, one_file)
                
            Data_Frame.to_excel(one_file) 
        
            print("All Image Features have been saved to " + one_file)
            print("Saved to directory: " + self.out_directory)
            
        if self.many_excel.get() == 1:
            
            print("All excel files saved to directory: " + self.out_directory)
            
        print('--END OF BATCH RUN--')
        
        #self.loading.set("Run Complete! Saved as: " + file)
        #self.Out.set("Saved to directory: " + self.out_directory)
    
    def OutputFile(self):
        
        self.excel_file = fd.askopenfilename()
        
        self.loading.set("Saving to " + self.excel_file)
        
    def OutputFolder(self):
        
        self.out_directory = fd.askdirectory()
        
        self.loading.set("Saving to " + self.out_directory)
    
    def QUIT(self):
        
        master.destroy()
    
master = tk.Tk()

app = Application(master=master)

app.mainloop()