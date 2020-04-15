import cv2
import os, argparse
from os import listdir
from multiprocessing.dummy import Pool as ThreadPool
import time
import numpy as np
import h5py

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', default='./Dataset/videos')
parser.add_argument('--output_dir', default='./Dataset/frames')
parser.add_argument('--height', type=int, default=360)
parser.add_argument('--width', type=int, default=640)
parser.add_argument('--num_workers', type=int, default=2)
args = parser.parse_args()

def read_frame(filename):
    # p = current_process()
    # print('process counter:', p._identity[0], 'pid:', os.getpid(), 'index:',index)
    video = cv2.VideoCapture(filename)
    fps = video.get(cv2.CAP_PROP_FPS)
    success, image = video.read()

    filename_split = os.path.splitext(os.path.basename(filename))
    filename_zero, fileext = filename_split
    count = 0
    while success:
        fname = "{}/frame_{:04d}.jpg".format(filename_zero, count)
        # print(fname)
        cv2.imwrite(os.path.join(args.output_dir , fname), image)
        success, image = video.read()
        print('file:',filename_zero, 'frame:', count)
        # print('process counter:', p._identity[0], 'pid:', os.getpid(), 'file:',filename_zero, 'frame:', count)
        count += 1

    print("Filename: " + filename)
    print("Frame per seconds: " + str(fps))

# videos = [os.path.join(args.input_dir, f) for f in listdir(args.input_dir) if os.path.isfile(os.path.join(args.input_dir, f))]

videos = []
for f in listdir(args.input_dir):
    if os.path.isfile(os.path.join(args.input_dir, f)):
        filename_split = os.path.splitext(f)
        filename_zero, fileext = filename_split
        os.makedirs(os.path.join(args.output_dir, filename_zero))
        videos.append(os.path.join(args.input_dir, f))

# Read frames from each video in separate processes
start = time.time()
pool = ThreadPool(args.num_workers) 
results = pool.map(read_frame, videos)
runtime = time.time() - start
print('Time taken: '+str(round(runtime, 3))+" seconds")

# h5_file = h5py.File('video.h5','w')
# images = [os.path.join(args.output_dir, f) for f in listdir(args.output_dir) if os.path.isfile(os.path.join(args.output_dir, f))]
# dataset_size = (len(images), args.height, args.width)
# imgs_dset = h5_file.create_dataset(images, dataset_size, np.uint8)