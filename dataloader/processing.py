
import torchvision.transforms as T
import torch
import numpy as np


SQUEEZENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
SQUEEZENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

class Processing():
    def __init__(self, size):
        self.size = size

    def preprocess(self, img):
        transform = T.Compose([
            T.Resize(self.size),
            T.ToTensor(),
            T.Normalize(mean=SQUEEZENET_MEAN.tolist(),
                        std=SQUEEZENET_STD.tolist()),
            T.Lambda(lambda x: x[None]),
        ])
        return transform(img)

    def deprocess(self, img):
        transform = T.Compose([
            T.Lambda(lambda x: x[0]),
            T.Normalize(mean=[0, 0, 0], std=[1.0 / s for s in SQUEEZENET_STD.tolist()]),
            T.Normalize(mean=[-m for m in SQUEEZENET_MEAN.tolist()], std=[1, 1, 1]),
            T.Lambda(self.rescale),
            T.ToPILImage(),
        ])
        return transform(img)

    def rescale(self, x):
        low, high = x.min(), x.max()
        x_rescaled = (x - low) / (high - low)
        return x_rescaled