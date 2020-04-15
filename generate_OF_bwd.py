import os
import PIL.Image as Image
import numpy as np
import cv2 as cv
from skimage.transform import resize

def save_flow(f1, f2, ct, dir_path, dir):
    # load image
    img1 = Image.open(os.path.join(dir_path,f1)).convert('RGB')
    img2 = Image.open(os.path.join(dir_path,f2)).convert('RGB')
    img1 = resize(np.asarray(img1), (360, 640, 3), anti_aliasing=True, preserve_range=True).astype(np.uint8)
    img2 = resize(np.asarray(img2), (360, 640, 3), anti_aliasing=True, preserve_range=True).astype(np.uint8)
    prvs = cv.cvtColor(img1,cv.COLOR_BGR2GRAY)
    next = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
    # calculate optical flow
    flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    out = os.path.join('./DataSet/flows/backward/', dir)
    if not os.path.exists(out):
        os.mkdir(out)
    res_path = os.path.join(out, 'flow_{:04d}_{:04d}.npy'.format(ct, ct-1))
    print('Saving: ', res_path)
    np.save(res_path, flow)


root = './Dataset/frames/'

for dir in os.listdir(root):
    if not dir.startswith('vid'): continue
    dir_path = os.path.join(root, dir)
    if os.path.exists(dir_path):
        frames = os.listdir(dir_path)
        frames.sort(reverse=True)
        ct = len(frames)-1
        f_next = frames[0]
        for f in frames[1:]:
            save_flow(f_next, f, ct, dir_path, dir)
            f_next = f
            ct -= 1

