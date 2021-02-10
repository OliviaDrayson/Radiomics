#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 14:50:24 2021

@author: oliviadrayson
"""

import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import scipy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure

import FeatureExtraction as fe

IMG, StudyDate, Name, ps, ss = fe.DICOM('604')
segmented = fe.Segment2(IMG)
#image3d = fe.ThreeDViewer(segmented)
RotatedLungs = scipy.ndimage.interpolation.rotate(segmented,270, axes=(2,1))

data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
X=np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]])
Y=np.array([[2, 2, 2], [1, 1, 1], [0, 0, 0]])

print("Making Mesh Now")

p = RotatedLungs
verts, faces, normals, values = measure.marching_cubes(RotatedLungs,method='lewiner',step_size=5)
mesh = Poly3DCollection(verts[faces], alpha=0.5)
mesh.set_facecolor('g')
#mesh.set_edgecolor('k')
 
print("Mesh Made")

#GUI-------------------------

tk_root = tk.Tk()

figure = Figure(figsize=(12, 8))
ax= figure.add_subplot(1, 1, 1, projection='3d')

#ax.plot_surface(data, X, Y, shade=True) ##replace

ax.add_collection3d(mesh)
    
ax.set_xlim(0, p.shape[0])
ax.set_ylim(0, p.shape[1])
ax.set_zlim(0, p.shape[2])
    
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

canvas = FigureCanvasTkAgg(figure, tk_root)

#canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
#canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
canvas.get_tk_widget().grid(row=1,columnspan=5)
canvas._tkcanvas.grid(row=0,columnspan=5)

canvas.mpl_connect('button_press_event', ax._button_press)
canvas.mpl_connect('button_release_event', ax._button_release)
canvas.mpl_connect('motion_notify_event', ax._on_move)

tk_root.mainloop()