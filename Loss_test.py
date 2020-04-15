from Loss import HybridLoss
import torch

params = {
    'style' : torch.rand((1,3,512,512)),
    'lmbda' : 1e4,
    'alpha' : 1,
    'beta' : 10,
    'gamma' : 1e-3,
    'c_layers' : [22],#ReLU4_2
    's_layers' : [3,8,13,22], #ReLU1_2, ReLU2_2, ReLU3_2, ReLU4_2,
    'eta' : 1

}
criterion = HybridLoss(**params)
content, content_prev = torch.rand(1, 3, 360, 640),torch.rand(1, 3, 360, 640)
styled, styled_prev = torch.rand(1, 3, 360, 640),torch.rand(1, 3, 360, 640)
fwd_flow = torch.rand(360, 640, 2)
bwd_flow = torch.rand(360, 640, 2)

loss = criterion(content, styled, content_prev, styled_prev, fwd_flow, bwd_flow)
print(loss)
