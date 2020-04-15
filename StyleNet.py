#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 13:50:10 2019

@author: wumeiqi
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules.instancenorm import InstanceNorm2d

#%%
class StyleNet(nn.Module):
    def __init__(self, initialize):
        super(StyleNet, self).__init__()
        # 1 input image channel, 16 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3)
        self.in1 = InstanceNorm2d(num_features=16)
        self.conv2 = nn.Conv2d(in_channels=16,out_channels=32, kernel_size=3, stride=2)
        self.in2 = InstanceNorm2d(num_features=32)
        self.conv3 = nn.Conv2d(in_channels=32,out_channels=48, kernel_size=3, stride=2)
        self.in3 = InstanceNorm2d(num_features=48)
        
        self.relu = nn.ReLU(inplace=True)
        
        self.resconv1 = nn.Conv2d(in_channels=48,out_channels=48, kernel_size=3,padding=(1,1))
        self.resconv2 = nn.Conv2d(in_channels=48,out_channels=48, kernel_size=3,padding=(1,1))
        self.resconv3 = nn.Conv2d(in_channels=48,out_channels=48, kernel_size=3,padding=(1,1))
        self.resconv4 = nn.Conv2d(in_channels=48,out_channels=48, kernel_size=3,padding=(1,1))
        self.resconv5 = nn.Conv2d(in_channels=48,out_channels=48, kernel_size=3,padding=(1,1))

        self.deconv1 = nn.ConvTranspose2d(in_channels=48,out_channels=32,kernel_size=3,stride=2)
        self.in4 = InstanceNorm2d(num_features=32)
        
        
        self.deconv2 = nn.ConvTranspose2d(in_channels=32,out_channels=16,kernel_size=3,stride=2)
        self.in5 = InstanceNorm2d(num_features=16)
        
        self.conv4 = nn.Conv2d(in_channels=16, out_channels=3, kernel_size=3)
        self.in6 = InstanceNorm2d(num_features=3)
        self.tanh = nn.Tanh()
        
        self.initialize = initialize
        if self.initialize:
            torch.nn.init.xavier_uniform_(self.conv1.weight)
            torch.nn.init.xavier_uniform_(self.conv2.weight)
            torch.nn.init.xavier_uniform_(self.conv3.weight)
            
            torch.nn.init.xavier_uniform_(self.resconv1.weight)
            torch.nn.init.xavier_uniform_(self.resconv2.weight)
            torch.nn.init.xavier_uniform_(self.resconv3.weight)
            torch.nn.init.xavier_uniform_(self.resconv4.weight)
            torch.nn.init.xavier_uniform_(self.resconv5.weight)
            
            torch.nn.init.xavier_uniform_(self.deconv1.weight)
            torch.nn.init.xavier_uniform_(self.deconv2.weight)
            
            torch.nn.init.xavier_uniform_(self.conv4.weight)
            
        

    def forward(self, x):
        # convolutional block
        x = self.relu(self.in1(self.conv1(x)))
        x = self.relu(self.in2(self.conv2(x)))
        x = self.relu(self.in3(self.conv3(x)))
        # print(x.shape)
        
        # residual block
        residual = x
        x = self.relu(self.in3(self.resconv1(x)))
        x = self.relu(self.in3(self.resconv2(x)))
        x = self.relu(self.in3(self.resconv3(x)))
        x = self.relu(self.in3(self.resconv4(x)))
        x = self.relu(self.in3(self.resconv5(x)+residual))
        # print(x.shape)


        # deconvolutional block
        x = self.relu(self.in4(self.deconv1(x)))
        x = self.relu(self.in5(self.deconv2(x)))
        # print(x.shape)
        
        # convolutional block
        x = self.tanh(self.in6(self.conv4(x)))
        # print(x.shape)
        
        return x
    

        
        
