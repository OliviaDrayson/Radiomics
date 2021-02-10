#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code for selecting slices

Created on Thu Jan 21 13:19:32 2021

@author: oliviadrayson
"""

import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
import scipy
from skimage.measure import label,regionprops
from skimage.morphology import closing, erosion, dilation, remove_small_objects

def convert(img, target_type_min, target_type_max, target_type):
    imin = img.min()
    imax = img.max()

    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    new_img = (a * img + b).astype(target_type)
    return new_img

def normalize(image):
        MIN_BOUND = -1000.0
        MAX_BOUND = 1000.0
        image = (image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
        image[image>1] = 1.
        image[image<0] = 0.
        return image

def SliceChoice(img3dR):
    
    Binary = (img3dR < -200) & (img3dR > -900)
    i = 0
    Slices = []
    AREAS = []
    SLICES = []
    
    for img_slice in Binary:
        
        binary = scipy.ndimage.morphology.binary_fill_holes(img_slice)
        binary = remove_small_objects(binary, min_size=500)
        binary = erosion(binary)
        
        label_image = label(binary)
        regions = regionprops(label_image)
        Areas = []
        
        for region in regions:
            Areas.append(region.area)
        
        Areas.sort()
        
        if len(Areas) > 2:
            for region in regions:
                if (region.area < 0.4*max(Areas)):
                    for coordinates in region.coords:
                        label_image[coordinates[0], coordinates[1]] = 0
    
        binary = label_image > 0
        binary = dilation(binary)
        
        label_image = label(binary)
        regions = regionprops(label_image)
        Areas = []
        
        for region in regions:
            Areas.append(region.area)
    
        x = Binary.shape[0]
        l = int(x/3)
        u = int(2*x/3)
        
        AREA = sum(Areas)
        
        #First take the middle third
        if i in range(l,u):
            if len(Areas) == 1:
                Slices.append([i,AREA])
                AREAS.append(AREA)
            
        i = i+1
        
    for Slice in Slices:
        if Slice[1] > 0.8*max(AREAS):
            SLICES.append(Slice[0])
  
    Chosen = min(SLICES)
    plt.imshow(Binary[Chosen])
    return Chosen

def SliceSegment(img3dR, slice_no, ps, ss):

    Image = img3dR[slice_no]
    
    #plt.imshow(Image, cmap=plt.cm.gray)
    
    #STEP TWO----------------------------------------------------------------------
    
    # Thresholding
    Image[Image <= -2000] = 0
    Image[Image >= 2000] = 0
    binary = (Image < -200) & (Image > -700)
    
    import scipy
    
    i = 1
    while i<5:
        binary = erosion(binary)
        i = i+1
    
    #Keeping only the biggest areas
    label_image = label(binary)
    regions = regionprops(label_image)
    areas = []
    kept_regions = []
    
    for region in regions:
        areas.append(region.area)
    
    for region in regions:
        if (region.area < 0.25*max(areas)):
            for coordinates in region.coords:
                label_image[coordinates[0], coordinates[1]] = 0
        else:
            kept_regions.append(region.area)
    
    binary2 = label_image > 0
    
    binary2 = scipy.ndimage.morphology.binary_fill_holes(binary2)
    i = 1
    while i<5:
        binary2 = dilation(binary2)
        i = i+1

    binary2 = closing(binary2)
    
    binary2 = scipy.ndimage.morphology.binary_fill_holes(binary2)
    
    Image2 = binary2 * Image
        
    """fig, ax1 = plt.subplots()
    ax1.imshow(Image, cmap=plt.cm.gray, interpolation='nearest')
    ax1.contour(binary2, [0.5], linewidths=1.2, colors='g')
    ax1.axis('off')
    plt.show"""
    #plt.savefig('png-copy.png')

    norm = normalize(Image)
    
    from skimage import color
    
    rgbIm = color.gray2rgb(norm)
    red_multiplier = [1, 0, 0]
    rgbIm[binary2, :] *= red_multiplier
    
    IMAGE = asarray(rgbIm)
    IMAGE = convert(IMAGE, 0, 255, np.uint8)

    ImageNaN = Image2
    
    # STEP THREE---------------------------------------------------------------
    import numpy as np
    
    #Area
    pixel = ss * ps[0]
    mmArea1 = pixel * kept_regions[0]
    if len(kept_regions) > 1:
        mmArea1 = mmArea1 + pixel*kept_regions[1]
    #print("Area(1) is:",mmArea1)
    
    binary_final = ImageNaN < 0
    area = sum(sum(binary_final))
    mmArea2 = area * pixel
    
    #print("Area(2) is:",mmArea2)
    
    #Mean
    ImageNaN[ImageNaN == 0] = np.nan    
    mean = np.nanmean(ImageNaN)
    #print("Mean is:",mean)
    
    #Median
    median = np.nanmedian(ImageNaN)
    #print("Median is:",median)
    
    #Standard Deviation
    std = np.nanstd(ImageNaN)
    #print("Standard Deviation is:",std)

    return IMAGE, mmArea1, mmArea2, mean, median, std






