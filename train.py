from Loss import HybridLoss
import torch
from torch import optim
from trainer import Trainer
import numpy as np
from StyleNet import StyleNet
from dataloader.processing import Processing
import PIL

SEED = 456 # 123
torch.manual_seed(SEED)
np.random.seed(SEED)

model = StyleNet(True)
# model = StyleNet(False)
# model.load_state_dict(torch.load('./Models/model_vid0_2_epoch1_iter540.pth'))


processer = Processing(size=(256, 256))
style = processer.preprocess(PIL.Image.open('./Dataset/style_images/candy.jpg'))
# style = io.imread('./Dataset/style_images/candy.jpg')
# style = resize(style, (256, 256, 3), anti_aliasing=True)
# style = torch.tensor(np.moveaxis(style, -1, 0)).unsqueeze_(0)
# print(type(style))
# print(style.shape)
paramsLoss = {
    'style' : style,
    'lmbda' : 1e4,
    'alpha' : 1,
    'beta' : 10,
    'gamma' : 1e-3,
    'c_layers' : [22],#ReLU4_2
    's_layers' : [3,8,13,22], #ReLU1_2, ReLU2_2, ReLU3_2, ReLU4_2,
    'eta' : 1
}
criterion = HybridLoss(**paramsLoss)

paramsTrainer = {
    'model': model,
    'criterion': criterion,
    'optimizer': optim.SGD(model.parameters(), lr=0.001, momentum=0.9),
    'style_image': style,
    'img_dir': './Dataset_test/',
    'epochs':2
}
trainer = Trainer(**paramsTrainer)

trainer.train()

