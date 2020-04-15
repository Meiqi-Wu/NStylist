#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 21:43:05 2019

@author: wumeiqi
"""


class Dataloader():
    def __init__(self, dataset, sampler):
        self.dataset = dataset
        self._sampleiter=iter(sampler)
        
    def __next__(self):
        video_idx, img_idx= next(self._sampleiter)
        img = self.dataset.get_item(video_idx, img_idx)
        img_next = self.dataset.get_item(video_idx, img_idx+1)
        concat = [img, img_next]
        return concat
        
        
        