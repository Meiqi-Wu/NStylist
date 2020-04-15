import numpy as np
import torch
import cv2

def applyflow(original, flow):
    original = np.asarray(original)
    flow = np.asarray(flow)
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
    
frame_prev=torch.rand((1,3,500,1000))
frame=torch.rand((1,3,500,1000))
fwd_flow=torch.rand(500,1000,2)
bck_flow=torch.rand(500,1000,2)


print(temporal_loss(frame_prev, frame, fwd_flow, bck_flow))