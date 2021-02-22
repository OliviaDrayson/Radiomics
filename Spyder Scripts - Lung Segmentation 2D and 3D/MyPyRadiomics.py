#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 17:25:58 2021

@author: oliviadrayson
"""

#Code for PYRADIOMICS

#!pip install SimpleITK
#!pip install pyradiomics

from __future__ import print_function
import sys
import os
import logging
import SimpleITK
import six
from radiomics import featureextractor, getFeatureClasses
import radiomics
import pandas as pd

#logging

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
