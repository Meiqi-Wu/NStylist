#!/usr/bin/env python
# coding: utf-8

import numpy as np
import torch
from torch import nn
import torchvision 
import cv2
import torch.nn.functional as F





class HybridLoss(nn.Module):
    
    def __init__(self, style, lmbda, alpha, beta, gamma, c_layers, s_layers, eta):
        super(HybridLoss, self).__init__()
        self.style = style
        self.lmbda = lmbda
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.c_layers = c_layers
        self.s_layers = s_layers
        self.eta = eta
        self.feat_net = extractor_net()
        self.feats_style = extract_features(self.style, self.feat_net)
        self.gram_style = []
        for l in self.s_layers:
            self.gram_style.append(gram_matrix(self.feats_style[l]))

        

    def forward(self, input, output, input_prev, output_prev, fwd_flow, bwd_flow):
        return hybrid_loss(input, output, input_prev, output_prev, fwd_flow, bwd_flow, feat_net=self.feat_net, gram_style=self.gram_style, 
                           lmbda=self.lmbda, alpha=self.alpha, beta=self.beta, gamma=self.gamma, 
                           c_layers=self.c_layers, s_layers=self.s_layers, eta=self.eta)


def hybrid_loss(input, output, input_prev, output_prev, fwd_flow, bwd_flow,feat_net,gram_style, lmbda, alpha, beta, gamma, c_layers, s_layers, eta):
    sp_loss = spatial_loss(feat_net, input, output, gram_style, alpha, beta, gamma, c_layers, s_layers, eta)
    # sp_loss_prev = spatial_loss(input_prev, output_prev, style, alpha, beta, gamma, c_layers, s_layers, eta)
    # sp_loss_total = sp_loss + sp_loss_prev
    tem_loss = temporal_loss(output_prev, output, fwd_flow, bwd_flow)
    
    return sp_loss + lmbda*tem_loss, sp_loss, tem_loss


def spatial_loss(feat_net, input, output, gram_style, alpha, beta, gamma, c_layers, s_layers, eta):
    feats_in = extract_features(input, feat_net)
    feats_out = extract_features(output, feat_net)
    
    content_acc = 0.0
    for l in c_layers:
        content_acc += content_loss(feats_in[l], feats_out[l])
        
    style_acc = 0.0
    for i, l in enumerate(s_layers):
        style_acc += style_loss(gram_style[i], feats_out[l])
        
    reg = tv_reg(output, eta)
    
    return alpha*content_acc + beta*style_acc + gamma*reg
    
# Feature extractor net
def extractor_net():
    net = torchvision.models.vgg19(pretrained=True).features.eval()
    for param in net.parameters():
        param.requires_grad = False
    return net

# Feature extractor layer util function
def extract_features(x, net):
    features = []
    feat = x.float()
    for module in net._modules.values():
        feat = module(feat)
        features.append(feat)
    return features


def content_loss(input, output):
    # N, C, H, W = input.size()
    # loss = torch.sum(torch.pow(input-output,2))
    # loss = loss/float(N*C*H*W)

    loss = F.mse_loss(input, output)
    
    return loss


# Gram matrix util function
def gram_matrix(features):
    N, C, H, W = features.size()
    # features = features.view(N, C,H*W)
    # gram_matrix = torch.zeros([N,C,C])
    # for i in range(N):
    #     gram_matrix[i,:] = torch.matmul(features[i,:],features[i,:].t())

    features = features.view(N*C, H*W)    
    gram_matrix = torch.mm(features, features.t())
    gram_matrix = gram_matrix/float(H*W)
    
    return gram_matrix



def style_loss(style_gram, output):
    output_gram = gram_matrix(output)
    loss = F.mse_loss(style_gram, output_gram)
    return loss


def tv_reg(img, eta):                                                       # Meiqi correction
    N, C, H, W = img.size()
    horz = torch.sum(torch.pow(img[:,:,1:,:]-img[:,:,:-1,:], 2))  
    vert = torch.sum(torch.pow(img[:,:,:,1:]-img[:,:,:,:-1], 2))
    loss = torch.pow(vert+horz, eta/2)
    return loss 





# Optical Flow util function
def optical_flow(frame_prev, frame):
    pass


def applyflow(original, flow):
    original = np.asarray(original.detach())   # 
    flow = np.asarray(flow.detach())
    y, x, _ = flow.shape
    loc_y = np.repeat(np.arange(y).reshape(y,1), x, axis=1)
    flow_y = (loc_y - flow[:,:,1]).astype(np.float32)
    loc_x = np.repeat(np.arange(x).reshape(1,x), y, axis=0)
    flow_x = (loc_x - flow[:,:,0]).astype(np.float32)
    mapped_img = cv2.remap(original, flow_x, flow_y, cv2.INTER_LINEAR)
    return torch.from_numpy(mapped_img)




def temporal_loss(frame_prev, frame, fwd_flow, bck_flow):
    dims = frame.size()
    if len(dims) == 4:
        _, C, H, W = dims
        frame_prev = frame_prev[0]
        frame = frame[0]
    else:
        C, H, W = dims
    
    warped_flow = applyflow(fwd_flow, bck_flow)
    
    def mag(tensor):
        return torch.pow(torch.norm(tensor, dim=-1), 2)
    
    disocc = mag(warped_flow+bck_flow) > (0.01*(mag(warped_flow) + mag(bck_flow))+0.5)
    
    fwd_flow_grad = torch.from_numpy(np.gradient(fwd_flow, axis=-1))
    motionbou = (mag(fwd_flow_grad[0]) + mag(fwd_flow_grad[1])) > (0.01*mag(bck_flow) + 0.002)
    
    c = torch.ones((H,W))
    c[disocc] = 0
    c[motionbou] = 0
    predict = applyflow(frame_prev*255, fwd_flow)/255.0
    
    loss = torch.sum(C*torch.pow((frame-predict), 2))                                             
    loss = loss/float(C*H*W)
    
    return loss
    

