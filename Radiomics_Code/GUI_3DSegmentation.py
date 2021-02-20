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

import matplotlib as plt

import SimpleITK as sitk
import math
import glob

import os
import openpyxl

import scipy
from scipy import ndimage

from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("3D Segmentation and Feature Extraction")
        
        #FRAMES
        style = 'flat'
        style2 = 'groove'
        
        #Section Frames
        self.BFrame = tk.LabelFrame(master, width = 400, height = 120, relief=style).grid(row=0, rowspan=4, columnspan=4)
        self.SFrame = tk.LabelFrame(master, width = 400, height = 190, relief=style).grid(row=4, rowspan=6, columnspan=4)
        self.RFrame = tk.LabelFrame(master, width = 400, height = 170, relief=style).grid(row=10, rowspan=5, columnspan=4)
        self.OFrame = tk.LabelFrame(master, width = 400, height = 280, relief=style).grid(row=15, rowspan=8, columnspan=4)
        
        #Large Frames
        self.MainFrame = tk.LabelFrame(master, width = 400, height = 760, relief='groove').grid(row=0, rowspan=24, column=0, columnspan=4)
        self.CFrame = tk.LabelFrame(master, width = 760, height = 760, relief='groove').grid(row=0, rowspan=24, column=4, columnspan=6)
        
        #Title Frames
        self.B_Title = tk.LabelFrame(master, width = 400, height = 30, relief=style2, bg="#C0C0C0").grid(row=0, rowspan=1, columnspan=4)
        self.S_Title = tk.LabelFrame(master, width = 400, height = 30, relief=style2, bg = "#C0C0C0").grid(row=4, rowspan=1, columnspan=4)
        self.R_Title = tk.LabelFrame(master, width = 400, height = 30, relief=style2, bg = "#C0C0C0").grid(row=10, rowspan=1, columnspan=4)
        self.O_Title = tk.LabelFrame(master, width = 400, height = 30, relief=style2, bg = "#C0C0C0").grid(row=15, rowspan=1, columnspan=4)
        
        # QUIT BUTTON
    
        self.Quit = tk.Button(master, text="QUIT", command=self.QUIT).grid(row=24, column=9, sticky='E')
        self.Name = tk.Label(master, text="by Olivia Drayson - drayson.o@mac.com").grid(row=24,column=8, sticky='E')
        
        self.canvas = tk.Canvas(self.CFrame, bg ="white", width=740, height=740)
        self.canvas.grid(row = 0, column = 4, rowspan=24, columnspan=6)
        
        # BATCH MODE FRAME
        
        self.BatchLabel = tk.Label(self.B_Title, text = "Batch Mode",font='Calibri 13 bold', bg="#C0C0C0").grid(row=0,columnspan=4)
        
        self.Batch = tk.Button(self.BFrame, text="Choose Images Folder", command=self.BatchMode)
        self.Batch.grid(row=1,column=0, columnspan=2)
        
        self.in_dir = StringVar()
        self.in_dir.set("Input folder: ")
        self.Label_Batch = tk.Label(self.BFrame, textvariable = self.in_dir, fg ="blue").grid(row = 2, columnspan=4)
        
        self.Batch_Run = tk.Button(self.BFrame, text = "Run", bg='green', command = self.BatchRun)
        self.Batch_Run.grid(row = 1, column = 2, columnspan = 2)
        
        self.BatchName = StringVar()
        self.BatchName.set("")
        self.EntryLabel = tk.Label(self.BFrame, text = "Enter Batch Name:").grid(row=3, column=0, columnspan = 2)
        self.BatchEntry = tk.Entry(self.BFrame, textvariable = self.BatchName).grid(row = 3, column = 2)
        
        # SINGLE MODE FRAME
        
        self.IndividualLabel = tk.Label(self.S_Title, text = "Single Mode", font='Calibri 13 bold', bg="#C0C0C0").grid(row=4,columnspan=4)
        
        self.openfile = tk.Button(self.SFrame, text = "Choose Image Directory", command=self.OpenFile)
        self.openfile.grid(row = 5,columnspan=4)
        
        self.prompt = StringVar()
        self.prompt.set("Name:")
        
        self.prompt2 = StringVar()
        self.prompt2.set("Date:")
        
        self.label = tk.Label(self.SFrame, textvariable=self.prompt)
        self.label.grid(row = 6, column=0, columnspan=4)
        
        self.label2 = tk.Label(self.SFrame, textvariable=self.prompt2)
        self.label2.grid(row = 7, column=0, columnspan=4)
        
        self.segment = tk.Button(self.SFrame, text ="3D Segmentation", command=self.Segment)
        self.segment.grid(row=8, column=0, columnspan=2)
        
        self.View = tk.Button(self.SFrame, text = "3D View", command=self.Viewer)
        self.View.grid(row=8,column=2, columnspan=2)
        
        self.FeatureE = tk.Button(self.SFrame, text = "Feature Extraction", command=self.FeatureExtract)
        self.FeatureE.grid(row=9,column=0, columnspan=4)
        
        # RADIOMICS FEATURE FRAME
        
        self.LabelFE = tk.Label(self.R_Title, text = "Radiomic Feature Customisation",font='Calibri 13 bold', bg="#C0C0C0")
        self.LabelFE.grid(row=10,column=0, columnspan=4)
        
        self.firstorder = IntVar()
        self.firstorder.set(1)
        self.FirstOrder = tk.Checkbutton(self.RFrame, text = "First Order", variable=self.firstorder)
        self.FirstOrder.grid(row=11, column=1, sticky='W')
        
        self.glcm = IntVar()
        self.glcm.set(1)
        self.Glcm = tk.Checkbutton(self.RFrame, text = "GLCM", variable=self.glcm)
        self.Glcm.grid(row=11, column=2, sticky='W')
        
        self.shape = IntVar()
        self.shape.set(1)
        self.Shape = tk.Checkbutton(self.RFrame, text = "Shape", variable=self.shape)
        self.Shape.grid(row=12, column=1, sticky='W')
        
        self.glrlm = IntVar()
        self.glrlm.set(1)
        self.Glrlm = tk.Checkbutton(self.RFrame, text = "GLRLM", variable=self.glrlm)
        self.Glrlm.grid(row=12, column=2, sticky='W')
        
        self.glszm = IntVar()
        self.glszm.set(1)
        self.Glszm = tk.Checkbutton(self.RFrame, text = "GLSZM", variable=self.glszm)
        self.Glszm.grid(row=13, column=1, sticky='W')
        
        self.wavelet = IntVar()
        self.wavelet.set(1)
        self.Wavelet = tk.Checkbutton(self.RFrame, text = "Wavelet", variable=self.wavelet)
        self.Wavelet.grid(row=13, column=2, sticky='W')
        
        self.Estimate = tk.Button(self.RFrame, text = "Estimate extraction time", command = self.Estimation)
        self.Estimate.grid(row=14, column=0, columnspan=2)
        
        self.time = StringVar()
        self.time.set("- mins -- secs")
        self.Time = tk.Label(self.RFrame, textvariable = self.time).grid(row=14, column=2, columnspan=2, sticky = 'W')
        
        # OUTPUT FRAME
        
        self.OutputLabel = tk.Label(self.O_Title, text="Output",font='Calibri 13 bold', bg="#C0C0C0").grid(row=15, columnspan=4)
                
        self.many_excel = IntVar()
        self.Many_Excel = tk.Checkbutton(self.OFrame, text = "Save to Separate Excel File(s)", variable=self.many_excel)
        self.Many_Excel.grid(row=16, column=1, columnspan=3, sticky='W')
        
        self.one_excel = IntVar()
        self.One_Excel = tk.Checkbutton(self.OFrame, text = "Create One Combined Excel File", variable=self.one_excel)
        self.One_Excel.grid(row=17, column=1, columnspan=3, sticky='W')
        
        self.add_excel = IntVar()
        self.Add_Excel = tk.Checkbutton(self.OFrame, text = "Add to Existing Excel File (select file below)", variable=self.add_excel)
        self.Add_Excel.grid(row=18, column=1, columnspan=3, sticky='W')
        
        self.OutputDirectory = tk.Button(self.OFrame, text = "Choose Output Directory", command=self.OutputFolder)
        self.OutputDirectory.grid(row=19, columnspan=4)
        
        self.loading = StringVar()
        self.loading.set("Output Directory:")
        self.Loading = tk.Label(master, textvariable = self.loading, fg ="blue").grid(row=20,columnspan=4)
        
        self.OUT = tk.Button(self.OFrame, text = "Choose Output File", command = self.OutputFile)
        self.OUT.grid(row=21, columnspan=4)
        
        self.L_outfile = StringVar()
        self.L_outfile.set("Add to File:")
        self.L_OutFile = tk.Label(master, textvariable = self.L_outfile, fg = "blue").grid(row=22,columnspan=4)
        
        #Disable inactive buttons
        self.activated = 0
        self.batch_activated = 0
        
        self.out_directory = 'a'
        self.excel_file = 'a'
        
        if self.activated == 0:
            self.segment["state"] = "disabled"
            self.View["state"] = "disabled"
            self.FeatureE["state"] = "disabled"
        
        if self.batch_activated == 0:
            self.Batch_Run["state"] = "disabled"
        
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
        
        if self.many_excel.get() == 1:        
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
    
        #Activate Run Button
        self.batch_activated = 1
        self.Batch_Run["state"] = "normal"
        
        BatchName = self.BatchName.get()
        
        #Get Image Directory
        self.bdirectory = fd.askdirectory()
        
        if self.out_directory == 'a': #If output directory is not defined
            self.out_directory = self.bdirectory
            
        print(BatchName + ' Batch Run Has Been Configured:')
        print('Input Image Directory: ' + self.bdirectory)
        print('Output Plot Directory: ' + self.out_directory)
        
        b_in_dir = str(self.bdirectory)
        
        if len(b_in_dir) > 35:
            b_in_dir = b_in_dir[-35:]
        
        self.in_dir.set("Input folder: ... " + b_in_dir)
      
    def BatchRun(self):
        
        bdirectory = self.bdirectory
        bdir = str(bdirectory) + "/*"
        bdir2 = str(bdirectory) + "/"
        
        counter = 0
        
        folders = glob.glob(bdir)
        folders = sorted(folders)
        
        if self.add_excel.get() == 1:
            print('Output Excel File: ' + self.excel_file)
            
        print("--STARTING BATCH RUN--")
        
        number = len(folders)
        
        for folder in folders:
        
            folder_name = folder.replace(bdir2, '')
            print("Now Segmenting: " + folder_name + ' (Image ' + str(counter+1) + ' of ' + str(number) + ')')
            
            #Getting DICOM Image from folder directory
            IMAGE, StudyDate, MouseName, ps, ss = fe.DICOM(folder)
            
            #Make Segmentation Mask
            Mask = fe.Segment4(IMAGE)
            
            #Generates 3D Plot and Saves to Output Directory
            fe.Viewer(Mask, folder_name, self.out_directory, self.BatchEntry.get())
                
            print("Calculating Features for: " + folder_name)
    
            Mask = Mask.astype(int)
        
            Image = sitk.GetImageFromArray(IMAGE)
            Mask = sitk.GetImageFromArray(Mask)

            CHECK_BOX = [self.firstorder.get(), self.glcm.get(), self.shape.get(), self.glrlm.get(), self.glszm.get(), self.wavelet.get()]
            
            #Radiomics Feature Extraction
            FeatureVector, df = fe.Radiomics(Image, Mask, CHECK_BOX)
            
            if self.many_excel.get() == 1: #If making an excel file for each image
                
                file = str(folder_name + "_" + StudyDate + "_output.xlsx")
                file = os.path.join(self.out_directory, file)
                df.to_excel(file)
                print("Features have been saved to " + file)
                   
            if self.one_excel.get() == 1: #If making one excel file with data from all images in batch
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
            
            if self.add_excel.get() == 1: #If adding all data to pre-existing excel file
            
                if self.excel_file == 'a': #If file is undefined 
                
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
                
                    ID = folder_name               
                
                    new_file = fe.ExcelFile(df, old_df, ID, StudyDate)
                    
                    new_file.to_excel(self.excel_file) 
            
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
      
    def OutputFile(self):
        
        self.excel_file = fd.askopenfilename()
        
        xdir = str(self.excel_file)
        
        if len(xdir) > 35:
            xdir = xdir[-35:]
                
        self.L_outfile.set("Add to File: ... " + xdir)
        
    def OutputFolder(self):
        
        self.out_directory = fd.askdirectory()
        pdir = str(self.out_directory)
        
        if len(pdir) > 35:
            pdir = pdir[-35:]
        
        self.loading.set("Output Directory:  ... " + pdir)
    
    def QUIT(self):
        
        master.destroy()
    
master = tk.Tk()

app = Application(master=master)

app.mainloop()