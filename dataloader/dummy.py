from dataset import VideoDataset
from sampler import VideoSampler
from torch.utils.data import DataLoader
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

PATH = './../Dataset_test/'

# temp = np.random.rand(360, 640, 3, 2)
# np.save(PATH+'flow/forward/forward-0000-0001.npy', temp)
# np.save(PATH+'flow/backward/backward-0001-0000.npy', temp)




dataset = VideoDataset(PATH)
sampler = VideoSampler(dataset, replacement=False) 
loader  = DataLoader(dataset, sampler=sampler, batch_size=1, num_workers=1)
dataloader_iterator = iter(loader)

for epoch in range(1):
    print('epoch=%d -------------------------'%(epoch))
    for i, data in enumerate(loader, 0):
        # print(data.shape)
        print(i)
        frames, fwd_flow, bwd_flow = data

        
        # print(fwd_flow.squeeze().shape)
        # print(bwd_flow.shape)
        print(frames.shape)

        


        
        if i>-1: break

        # print(image1, image2)

        # im_show('image1', tensor_to_img(image1), resize=6 )
        # im_show('image2', tensor_to_img(image2), resize=6 )
        # cv2.waitKey(1)
# dd=0