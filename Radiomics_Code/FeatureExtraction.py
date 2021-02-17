#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 18:12:36 2021

@author: oliviadrayson
"""

from __future__ import print_function
import logging
import six
from radiomics import featureextractor, getFeatureClasses
import radiomics
import pandas as pd
import glob
import pydicom as dicom
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import ndimage
from skimage.measure import label,regionprops
from skimage.morphology import erosion, dilation, remove_small_objects #closing

from skimage.segmentation import clear_border
from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import statistics as stats

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
    
    return img3dR, StudyDate, Name, ps, ss

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
    
def GetImage(img3dR, slice_no):
    
    IMAGE = img3dR[slice_no]
    IMAGE = normalize(IMAGE)
    IMAGE = convert(IMAGE, 0, 255, np.uint8)
    return IMAGE
    
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
    return Chosen

def Viewer(Mask, folder_name, directory):
    
    Mask = scipy.ndimage.interpolation.rotate(Mask,270, axes=(2,1))
    
    verts, faces, normals, values = measure.marching_cubes(Mask,method='lewiner',step_size=2)

    p = Mask
    
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    title = "Segmented Lungs of " + folder_name + " in 3D"
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
    
    return fig
    
def Segment4(img3dR):
    
    #Make binary and threshold
    Axial = img3dR.transpose(1,0,2)
    
    Segmented = []
    Largest = []
    Shifted = 0
    
    for im in Axial:   
                
        binary = (im < -200) & (im > -900)
        cleared = clear_border(binary)
        label_image = label(cleared)
        
        regions = regionprops(label_image)
        
        #Keeping only n largest areas
        areas = [r.area for r in regions]
        areas.sort()
        n = 2 #keeping top n

        if len(areas) > n:
            for region in regionprops(label_image):
                if region.area < areas[-n] or region.area < 300:
                    for coordinates in region.coords:                
                        label_image[coordinates[0], coordinates[1]] = 0
                if region.area == max(areas):
                    Largest.append(region.centroid[1])
                        
        im = label_image > 0
        
        label_image = label(im)
        regions = regionprops(label_image)
        
        #now only keeping central objects
                 
        centres = [r.centroid for r in regions]
    
        def modulus(centre):
            
            if Shifted == 0:
                x = centre[0] - (im.shape[0]/2)
                y = centre[1] - (im.shape[1]/2)
            else:
                x = centre[0] - (im.shape[0]/2)
                y = centre[1] - Shifted
        
            mod = x**2 + y**2
            mod = mod**0.5
            return mod

        mods = [modulus(c) for c in centres]
        mods.sort()

        for region in regions:
            centre = region.centroid
            mod = modulus(centre)
            
            #length = 3*max(im.shape)/8 #inner 3/4 of the image
            length = max(im.shape) #inner 3/4 of the image
            
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
    
    Largest = round(stats.mean(Largest))
    Shifted = Largest
    
    Segmented = []
    
    for im in Coronal:
        
        im = clear_border(im)
        label_image = label(im)
        regions = regionprops(label_image)
        
        for region in regions:
            centre = region.centroid
            mod = modulus(centre)
            
            length = max(im.shape)/3 #inner two thirds of the image
        
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
    
    Segmented = ndimage.binary_erosion(Segmented, iterations=5)
    Segmented = ndimage.binary_fill_holes(Segmented)
    Segmented = ndimage.binary_dilation(Segmented, iterations=5)
    
    return Segmented

def MeshGeneration(Image):
    
    RotatedLungs = scipy.ndimage.interpolation.rotate(Image,270, axes=(2,1))
    
    verts, faces, normals, values = measure.marching_cubes(RotatedLungs,method='lewiner',step_size=5)
    mesh = Poly3DCollection(verts[faces], alpha=0.5)
    mesh.set_facecolor('g')
    
    return mesh
    
def Radiomics(imageName, maskName, CHECK_BOX):

    [firstorder, glcm, shape, glrlm, glszm, wavelet] = CHECK_BOX
    
    # Get the PyRadiomics logger (default log-level = INFO)
    logger = radiomics.logger
    logger.setLevel(logging.ERROR)  # set level to DEBUG to include debug log messages in log file
    
    # Write out all log entries to a file
    handler = logging.FileHandler(filename='testLog.txt', mode='w')
    formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
        
    # Alternative: use hardcoded settings (separate for settings, input image types and enabled features)
    settings = {}
    settings['binWidth'] = 25
    settings['resampledPixelSpacing'] = None
    # settings['resampledPixelSpacing'] = [3, 3, 3]  # This is an example for defining resampling (voxels with size 3x3x3mm)
    settings['interpolator'] = 'sitkBSpline'
    settings['verbose'] = True
    
    extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
    
    if wavelet == 1:
        extractor.enableImageTypeByName('Wavelet')
    
    #print('Enabled input images:')
    for imageType in extractor.enabledImagetypes.keys():
        #print('\t' + imageType)
        
        # Disable all classes
        extractor.disableAllFeatures()
        
        # Enable all features in firstorder
        if firstorder == 1:
            extractor.enableFeatureClassByName('firstorder')
        if glcm == 1:
            extractor.enableFeatureClassByName('glcm')
        if shape == 1:
            extractor.enableFeatureClassByName('shape')
        if glrlm == 1:
            extractor.enableFeatureClassByName('glrlm')
        if glszm == 1:
            extractor.enableFeatureClassByName('glszm')
            
        featureVector = extractor.execute(imageName, maskName)
        
    # Show output
    df = pd.DataFrame(columns=["Feature", "Value"])

    for featureName in featureVector.keys():
        n = df.shape
        n = n[0] #number of rows
        
        df.loc[n] = [featureName, featureVector[featureName]]
        #print('Computed %s: %s' % (featureName, featureVector[featureName]))
        
    writer = pd.ExcelWriter('Output.xlsx', engine='xlsxwriter')
    df.to_excel(writer, 'Sheet1', index = False)
    writer.save()    
        
    return featureVector, df
    
def ExcelFile(new_df, old_df, ID, StudyDate): #new df and old df to be added to
    
    #Function either combines all batch run features or appends a single run to an existing excel file
    new_row = [ID, StudyDate]
    
    for feature in old_df.columns:
        
        for feat in new_df["Feature"]:
            
            if feat == feature:
                
                index = new_df.index[new_df["Feature"] == feature].tolist()
                index = index[0]
                
                value = new_df["Value"].loc[index]
                
                new_row.append(value)
    
    n = old_df.shape
    n = n[0] #the number of items in the data frame already

    old_df.loc[n] = new_row
    
    return old_df


