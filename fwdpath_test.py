


import time
from skimage import io
from skimage.transform import resize
import skimage
import torch
import numpy as np
import os
from StyleNet import StyleNet
from dataloader.processing import Processing
import PIL

nsub_frames = 2

model = StyleNet(False)
model.load_state_dict(torch.load('./Models/model_vid0_2_epoch1_iter20.pth'))


processer = Processing((360, 640))

# make a directory for output
if not os.path.exists('styled_out'):
    os.mkdir('styled_out')


for vid in os.listdir('./Dataset_test/frames/'):
    if not vid.startswith('vid'): continue
    print('\n')
    print(vid)
    if not os.path.exists('./styled_out/'+vid):
        os.mkdir('./styled_out/'+vid)
    start = time.time()

    frames = os.listdir('./Dataset_test/frames/'+vid)
#    frames.sort(key=lambda x: int(x.split('.')[0][6:]))
    nframe = len(frames)
    for k in range(0, nframe, nsub_frames):
        frames_sub = frames[k:min(k+nsub_frames, nframe)]
        imgs = torch.empty((nsub_frames,3,360, 640))
    #    imgs = np.empty((4,360, 640, 3))
        for i, frame in enumerate(frames_sub):
            filename = './Dataset_test/frames/'+vid+'/'+frame
            img = processer.preprocess(PIL.Image.open(filename))
            imgs[i] = img
            
        styled = model(imgs)
        print(styled.shape)
        styled=styled.detach()
        for i, frame in enumerate(frames_sub):
            # img = styled[i].unsqueeze_(0)
            # print(img.shape)
            img = processer.deprocess(styled[i].unsqueeze_(0))
            # img = np.moveaxis(img, 0, -1)
            # img = resize(img, originalSize, anti_aliasing=True)
            # img = (img-img.min())/(img.max()-img.min())
            img = skimage.img_as_ubyte(img)
            io.imsave('./styled_out/'+vid+'/'+frame, img)
        
        print('Have processed ', k+nsub_frames, ' out of ', nframe,' frames in ', time.time()-start, 'seconds')
        break
    break



    
    