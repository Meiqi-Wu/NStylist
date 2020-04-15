from torch.utils.data import Dataset
import os
import numpy as np
from dataloader.processing import Processing
import PIL
import torch



class VideoDataset(Dataset):
    """
    Dataset class
    """
    def __init__(self, img_dir):
        """
        :
        """
        self.img_dir = img_dir
        self.processor = Processing(size=(360, 640))
        
    def __getitem__(self, idx):
        """
        :idx: tuple (v_idx,f_idx)
        :v_idx: integer, index of vedio
        :f_idx: integer, index of frame
        :return: an transformed image 
        """
#        print(idx)
        v_idx, f_idx = idx
        fname = 'frames/vid_{:02d}/frame_{:04d}.jpg'.format(v_idx, f_idx)
        img_name = os.path.join(self.img_dir, fname)
        image1 = self.processor.preprocess(PIL.Image.open(img_name))
        # image1 = io.imread(img_name)
        # image1 = resize(image1, (360, 640, 3), anti_aliasing=True)
        # image1 = img_name

        fname = 'frames/vid_{:02d}/frame_{:04d}.jpg'.format(v_idx, f_idx+1)
        img_name = os.path.join(self.img_dir, fname)
        image2 = self.processor.preprocess(PIL.Image.open(img_name))
        # image2 = io.imread(img_name)
        # image2 = resize(image2, (360, 640, 3), anti_aliasing=True)
        # image2 = img_name
        
        images = torch.cat((image1, image2), 0)

        # images = np.array([image1, image2])
        # images = np.moveaxis(images, -1, 1)
        # print(images.shape)

        fname = 'flows/forward/vid_{:02d}/flow_{:04d}_{:04d}.npy'.format(v_idx, f_idx, f_idx+1)
        flow_name = os.path.join(self.img_dir, fname)
        fwd_flow = np.load(flow_name)

        fname = 'flows/backward/vid_{:02d}/flow_{:04d}_{:04d}.npy'.format(v_idx, f_idx+1, f_idx)
        flow_name = os.path.join(self.img_dir, fname)
        bwd_flow = np.load(flow_name)



        return images, fwd_flow, bwd_flow
        # return images


    
