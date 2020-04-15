from Loss import HybridLoss
import torch
from torch import optim
from trainer import Trainer
import numpy as np
from StyleNet import StyleNet
from skimage import io
from skimage.transform import resize
from dataloader.processing import Processing
import PIL

# log = open('log_train.txt', 'w')
# log.write('[Epoch {}, idx {}] loss:{} sp_loss:{} tem_loss{}'.format(1+1, 2+1, 0.22233/20, 3.666/20, 6.555555/20))
# log.close()

processer = Processing(size=(256, 256))
style = processer.preprocess(PIL.Image.open('./Dataset/style_images/candy.jpg'))
print(style.size())