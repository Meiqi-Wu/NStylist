from flask import Flask, render_template, Markup, request, redirect, url_for, flash, session
import os, errno
import glob
import datetime
import subprocess
import torch
import cv2
import time
import numpy as np
import glob
from skimage import io
from skimage.transform import resize
import skimage
from os.path import isfile, join
from threading import Thread
import sys
sys.path.append("..")
import StyleNet as s
import transformer as t

# combine the styled frames into videos

pathIn = 'upload_dir/'
pathOut = 'style_video.mp4'
fps = 25.0
frame_array = []
print(1)
files =  glob.glob('upload_dir/styled_out/*.jpg')#[f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
# print(files)
#for sorting the file names properly
files.sort(key = lambda x: int(x.split("_")[-1].replace(".jpg","")))#[file_length+3:-4]))

for i in range(len(files)):
    filename=files[i]
    print(filename)
    print(filename)
    #reading each files
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    print(filename)
    #inserting the frames into an image array
    frame_array.append(img)

# fourcc = cv2.VideoWriter_fourcc(*'MPEG')
# out = cv2.VideoWriter(pathOut,fourcc, 20.0, (640,480))
out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
out.release()