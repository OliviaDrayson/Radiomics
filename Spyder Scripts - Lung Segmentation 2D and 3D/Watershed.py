#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 12:44:17 2021

@author: oliviadrayson
"""

import matplotlib.pyplot as plt
import pydicom as dicom
import glob
import numpy as np
import scipy
from skimage.segmentation import clear_border
from skimage.measure import label,regionprops
from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt

from skimage import measure, morphology, segmentation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from tkinter import filedialog as fd

no = 125

directory = '/Users/oliviadrayson/Desktop/CBCT_Females/725_Images/725 W+21'
print(directory)

def DICOM(directory):
    # Converts DICOM image to a 3D array in the coronal plane
    
    suffix = '/*.dcm'
    imagepath = directory + suffix
    
    slices = []
    files = sorted(glob.glob(imagepath))
        
    for fname in files: 
        ds = dicom.dcmread(fname)
        slices.append(ds)
    
    StudyDate = ds.StudyDate
    Name = ds.PatientName
                
    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)
        
    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d
    
    ps = slices[0].PixelSpacing
    ss = slices[0].SliceThickness
    
    #plt.imshow(slices[100].pixel_array, cmap=plt.cm.gray)
                    
    # Rotate image 90 degrees
    img3dR = scipy.ndimage.interpolation.rotate(img3d,90,axes=(2,1))
    
    img3dR[img3dR < -2000] = 0
    
    return img3dR #StudyDate, Name, ps, ss

IMAGE = DICOM(directory)

Axial = IMAGE.transpose(1,0,2)

print(IMAGE[no].shape)
print(Axial[no].shape)

plt.imshow(Axial[no])
plt.show()

#Thresholding

def threshold(image, counter):
    
    binary = (image < 0) & (image > -900)
 
    cleared = clear_border(binary)
    label_image = label(cleared)
        
    regions = regionprops(label_image)
        
    #Keeping only n largest areas
    areas = [r.area for r in regions]
    areas.sort()

    n = 2 #keeping top n areas

    if len(areas) > n:
        for region in regionprops(label_image):
            if region.area < areas[-n] or region.area < 100:
                for coordinates in region.coords:                
                    label_image[coordinates[0], coordinates[1]] = 0
                   
    
    im = label_image > 0
    regions = regionprops(label_image)
    
    # now removing most distant objects
                 
    centres = [r.centroid for r in regions]
    
    centres_0 = [c[0] for c in centres]
    centres_1 = [c[1] for c in centres]
    
    def modulus(centre):
        
        x = centre[0] - (image.shape[0]/2)
        y = centre[1] - (image.shape[1]/2)
        
        mod = x**2 + y**2
        mod = mod**0.5
        return mod

    mods = [modulus(c) for c in centres]
    mods.sort()

    if counter == 150:
        print(mods)

    for region in regions:
        centre = region.centroid
        mod = modulus(centre)
        
        #length = (image.shape[0] + image.shape[1])/8 #inner half of the image
        length = max(image.shape)/3 #middle third
        
        if len(mods) > 1:
            if mod > length or mod > 1.5*mods[1]:
                for coordinates in region.coords:                
                    label_image[coordinates[0], coordinates[1]] = 0
        else:
            if mod > length:
                for coordinates in region.coords:                
                    label_image[coordinates[0], coordinates[1]] = 0

    im = label_image > 0

    return im

def THRESHOLD(IMAGE):
    
    Segmented = []
    
    for im in IMAGE:
        
        binary = (im < 0) & (im > -900)
        cleared = clear_border(binary)
        label_image = label(cleared)
        
        regions = regionprops(label_image)
        
        #Keeping only n largest areas
        areas = [r.area for r in regions]
        areas.sort()

        n = 2 #keeping top n areas

        if len(areas) > n:
            for region in regionprops(label_image):
                if region.area < areas[-n] or region.area < 200:
                    for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0
                   
        im = label_image > 0
        
        label_image = label(im)
        regions = regionprops(label_image)
        
        #now only keeping central objects
                 
        centres = [r.centroid for r in regions]
    
        def modulus(centre):
            
            x = centre[0] - (im.shape[0]/2)
            y = centre[1] - (im.shape[1]/2)
        
            mod = x**2 + y**2
            mod = mod**0.5
            return mod

        mods = [modulus(c) for c in centres]
        mods.sort()

        for region in regions:
            centre = region.centroid
            mod = modulus(centre)
            
            length = max(im.shape)/3 #inner 2/3 of the image
            
            if len(mods) > 1:
                if mod > length or mod > 1.5*mods[1]:
                    for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0
            else:
                if mod > length:
                     for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0
                    
        im = label_image > 0
        Segmented.append(im)
    
    Segmented = np.stack([s for s in Segmented])
    
    Coronal = Segmented.transpose(1,0,2) #back to coronal
    Segmented = []
    
    for im in Coronal:
        
        im = clear_border(im)
        label_image = label(im)
        regions = regionprops(label_image)
                            
        for region in regions:
            centre = region.centroid
            mod = modulus(centre)
            
            length = 3*max(im.shape)/8 #inner three quarters of the image
        
            if len(mods) > 1:
                if mod > length or mod > 1.5*mods[1]:
                    for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0
            else:
                if mod > length:
                     for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0

        im = label_image > 0
        Segmented.append(im)
        
    Segmented = np.stack([s for s in Segmented])
    Segmented = Segmented.transpose(1,0,2)
    
    Segmented = ndimage.binary_dilation(Segmented, iterations=10)
    Segmented = ndimage.binary_fill_holes(Segmented)
    Segmented = ndimage.binary_erosion(Segmented, iterations=10)
    
    return Segmented
    
def Segment4(img3dR):
    
    #Make binary and threshold
    Axial = img3dR.transpose(1,0,2)
    
    Segmented = []
    
    for im in Axial:   
        
        binary = (im < 0) & (im > -900)
        cleared = clear_border(binary)
        label_image = label(cleared)
        
        regions = regionprops(label_image)
        
        #Keeping only n largest areas
        areas = [r.area for r in regions]
        areas.sort()
        n = 2 #keeping top n

        if len(areas) > n:
            for region in regionprops(label_image):
                if region.area < areas[-n] or region.area < 200:
                    for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0
                        
        im = label_image > 0
        
        label_image = label(im)
        regions = regionprops(label_image)
        
        #now only keeping central objects
                 
        centres = [r.centroid for r in regions]
    
        def modulus(centre):
            
            x = centre[0] - (im.shape[0]/2)
            y = centre[1] - (im.shape[1]/2)
        
            mod = x**2 + y**2
            mod = mod**0.5
            return mod

        mods = [modulus(c) for c in centres]
        mods.sort()

        for region in regions:
            centre = region.centroid
            mod = modulus(centre)
            
            length = max(im.shape)/3 #inner 2/3 of the image
            
            if len(mods) > 1:
                if mod > length or mod > 1.5*mods[1]:
                    for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0
            else:
                if mod > length:
                     for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0
                    
        im = label_image > 0
        Segmented.append(im)
        
    Segmented = np.stack([s for s in Segmented])
    
    Coronal = Segmented.transpose(1,0,2) #back to coronal
    Segmented = []
    
    for im in Coronal:
        
        im = clear_border(im)
        label_image = label(im)
        regions = regionprops(label_image)
        
        for region in regions:
            centre = region.centroid
            mod = modulus(centre)
            
            length = 3*max(im.shape)/8 #inner three quarters of the image
        
            if len(mods) > 1:
                if mod > length or mod > 1.5*mods[1]:
                    for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0
            else:
                if mod > length:
                     for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0

        im = label_image > 0
        Segmented.append(im)
        
    Segmented = np.stack([s for s in Segmented])
    
    Segmented = ndimage.binary_dilation(Segmented, iterations=10)
    Segmented = ndimage.binary_fill_holes(Segmented)
    Segmented = ndimage.binary_erosion(Segmented, iterations=10)
    
    Segmented = Segmented.transpose(1,0,2)

    return Segmented

"""counter = no
test_threshold = threshold(Axial[no], counter) * Axial[no]

# Threshold 3D

Segmented = []

counter = 0

for image_slice in Axial:
    counter += 1
    Segmented.append(threshold(image_slice, counter))
    
Segmented = np.stack([s for s in Segmented])

Segmented = ndimage.binary_dilation(Segmented, iterations=10)
Segmented = ndimage.binary_fill_holes(Segmented)
Segmented = ndimage.binary_erosion(Segmented, iterations=10)"""

##

#Segmented = THRESHOLD(Axial)
Segmented = Segment4(IMAGE)

print("Threshold Lung")
plt.imshow(Segmented[no], cmap='gray')
plt.show() 

#### 3D View

Segmented = Segmented.transpose(1,0,2)

Segmented = scipy.ndimage.interpolation.rotate(Segmented, 270, axes=(2,1))
    
verts, faces, normals, values = measure.marching_cubes(Segmented,method='lewiner',step_size=2)

p = Segmented
    
fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111, projection='3d')
    
title = "Segmented Lungs in 3D"
ax.set_title(title, fontsize=15)
    
mesh = Poly3DCollection(verts[faces], alpha=0.5)
ax.add_collection3d(mesh)

ax.set_xlim(0, p.shape[0])
ax.set_ylim(0, p.shape[1])
ax.set_zlim(0, p.shape[2])
    
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

fname = directory + "/" + title + ".png"
plt.savefig(fname)

