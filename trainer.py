
"""
Created on Wed Oct 23 12:04:16 2019

@author: wumeiqi
"""

import numpy as np
import torch 
from torch.utils.data import DataLoader
from dataloader.dataset import VideoDataset
from dataloader.sampler import VideoSampler
# from torchvision.transforms import Resize
import torch.nn.functional as F
import time

class Trainer():
    """
    Trainer class
    """
    def __init__(self, model, criterion, optimizer, img_dir, style_image, epochs):
        self.model = model
        self.criterion = criterion # the loss function
        self.dataset = VideoDataset(img_dir)
        self.sampler = VideoSampler(self.dataset, replacement=True) 
        self.loader  = DataLoader(self.dataset, sampler=self.sampler, batch_size=1, num_workers=1)
        self.optimizer = optimizer
        self.style_image = style_image
        self.epochs = epochs
        
    def train(self):
        """
        Full training logic
        """
        # start = time.time()
        log = open('log_train.txt', 'w')
        for epoch in range(self.epochs):    
            running_loss = 0.0
            running_sp_loss = 0.0
            running_tem_loss = 0.0
            
            for idx, data in enumerate(self.loader):
                frames=data[0].squeeze().float()
                fwd_flow, bwd_flow = data[1].squeeze(), data[2].squeeze()
                
                # get the inputs; frames is torch.tensor of size 2x3x360x640, containing 2 adjacent frames xt_1, xt
                # fwd_flow, bwd_flow both are torhc.tensir of size 360x640x2
                
                # zero the parameter gradient
                self.optimizer.zero_grad()
                
                # forward + backward + optimize
                frames_styled = self.model(frames)
                frames_styled = F.interpolate(frames_styled, size=(360, 640))
                xt_1, xt = torch.unsqueeze(frames[0], 0), torch.unsqueeze(frames[1], 0)
                xt_1_hat, xt_hat = torch.unsqueeze(frames_styled[0], 0), torch.unsqueeze(frames_styled[1],0)

                hy_loss, sp_loss, tem_loss = self.criterion(xt, xt_hat, xt_1, xt_1_hat, fwd_flow, bwd_flow)
                hy_loss.backward()
                
                self.optimizer.step()
                
                # print statistics
                running_loss += hy_loss
                running_sp_loss += sp_loss
                running_tem_loss += tem_loss
                if (idx+1)%20 == 0:
                    print('[Epoch {}, idx {}] loss:{:10.6f} temp loss:{:10.6f}'.format(epoch+1, idx+1, running_loss/20, running_tem_loss/20))
                    # print('Time elasped: ', time.time()-start, ' s')
                    log.write('[Epoch {}, idx {}] loss:{} sp_loss:{} tem_loss{}'.format(epoch+1, idx+1, running_loss/20, running_sp_loss/20, running_tem_loss/20))
                    log.write('\n')
                    running_loss = 0.0
                    running_sp_loss = 0.0
                    running_tem_loss = 0.0
                    torch.save(self.model.state_dict(), './Models/model_vid0_2_epoch{}_iter{}.pth'.format(epoch+1, idx+1))
                
        
        print('Finished training epoch {}'.format(epoch))

        log.close()
        # save the trained model


            
        
            
            