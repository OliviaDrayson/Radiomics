# Radiomics

## by Olivia Drayson

3D Segmentation and Radiomic feature extraction for CT scans of whole lungs

## Information for Use

This is a GUI for analysing CT scans of lungs. Requires python and at least one DICOM image. Only works on DICOM images for now. 

Segmentation is done using thresholding between -900 and -200 HU. This is currently not changeable. 

Extraction of radiomic features is done using the library 'pyradiomics'. 
Wavelet filtering optional and user can choose to include or exclude first order, glcm, shape, glrlm and glszm features. 

Output can be saved to excel files. User has option between creating a file for a single extraction or combining results from multiple images in a single excel file. 

User can analyse a single image at a time or undergo a batch run. Batch run requires a folder containing only DICOM image folders. The names of the folders will be used as the IDs of the images.

Single image mode allows for better viewing of the segmentation both a 2D slice and a 3D mesh volume. 

## How to Use

### Batch Mode

Everything is automated in batch mode so you only need to select the desired output (in output section), customise the extraction (in Radiomics Feature Customisation section) and then select the folder containing the images to be segmented (in batch mode section).

Start in the output section. You can create a file for each image extraction and you can create one file containing all extraction results from all images.

(Optional) Then make changes to the feature extraction settings by selecting the checkboxes in the Radiomics Feature Customisation section. The default is to extract all feature types including wavelet filtering. 

(Optional) If you would like to save the excel files to a directory different to the current working directory click on 'Choose Output Directory'. The default is the current working directory. The terminal will print the name of the file once it has been created.

Now click on 'Choose Images Folder' to select the images to analyse. As mentioned above the folder should only contain the DICOM image folders you want to segment.

Then the software automatically runs segmentation, feature extraction and saving output to excel file(s). The software will print to the terminal when the extraction is complete and a plot of each segmentation will be shown.

### Single Mode

Single mode allows for a closer inspection of the 3D segmentation and future versions will allow for more customisation of the segmentation compared to batch mode.

Like batch mode, it is recommended to choose your output format and directory first. This can be done at any stage before feature extraction though. You can save the output to a single excel file or append it to an existing excel file. See the requirements for adding to an existing excel file below for more details.

Then load the image using 'Choose Image Directory'. This will show a slice of the DICOM to the window as chosen by the software to be near the middle of the lungs. 
Segment the whole image by clicking '3D Segmentation'. This button will be enabled once an image has been loaded. 

(Optional) View a 3D plot of the segmentation by clicking '3D Viewer'. Note the 3D volume shown is coarser than the actual mask (element size of 3) to allow for manoevrability of the image. You can rotate the image by clicking and dragging across the window. 

(Optional) For single mode you can estimate the length of time the extraction will take using the 'Estimate Extraction Time' button. 

Once the extraction has been customised using the checkbuttons you can click 'Feature Extraction' to generate the features and save them to an excel file.

### Requirements for Adding to an Existing Excel File (Single Mode)

This feature creates a row for the image extraction results and appends that row to the bottom of the existing excel file. Therefore the existing file must be in .xlsx format and must contain the features as columns. There should be the same features in the columns as you extract from the image. There should be an index column and then the first two columns must be called 'Image ID' and 'Study Date'. The feature column names must be in the format:

filtertype_featuretype_FeatureName

such as: 'original_shape_MeshVolume' or: 'wavelet-LLH_firstorder_Kurtosis'

The feature names in any excel file outputted by the software will follow this format. 

Note: If a batch mode is initiated on one image the 'combined file' option will produce an excel file in the correct format. If you are having difficulty making an appropraite excel file from scratch I recommend do a batch run on the image first and then append all future results to that file. 

## Final Remarks

This software is designed to assist with data extraction for a machine learning radiomics analysis of whole lungs. Future versions may include other data formats, other organs or additional customisation features.

For questions or if you encounter any issues or find bugs in the software please contact myself at:

drayson.o@mac.com 

or contact me on github @OliviaDrayson

Thank you for using my GUI! I hope you find it useful.