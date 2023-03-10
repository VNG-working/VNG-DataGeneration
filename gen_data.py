from ast import Sub
from copy import deepcopy
import numpy as np
from time import time
import json
import os
import cv2

def mapping(boxes, position):
    '''
    Args: 
        boxes: List boxes of smaller module
        position: (x, y) position where to paste module ==> top-left
    Output: 
        list boxes in larger coordinate space
    Note that function not change order of box in list
    '''
    boxes = np.array(boxes) 
    new_boxes = np.copy(boxes)
    new_boxes[:, 0] = boxes[:, 0] + position[0]
    new_boxes[:, 1] = boxes[:, 1] + position[1]
    return new_boxes

def resize(new_shape, img, boxes):
    new_h, new_w = new_shape
    h, w = img.shape[:2]
    scale_x, scale_y = new_w / h, new_h / h
    new_img = cv2.resize(img, (new_w, new_h))
    if isinstance(boxes, list):
        new_boxes = [[x1*scale_x, y1*scale_y, x2*scale_x, y2*scale_y] for (x1, y1, x2, y2) in boxes]
    else: #numpy array
        new_boxes = np.copy(boxes)
        new_boxes[:, 0] = boxes[:, 0] * scale_x
        new_boxes[:, 1] = boxes[:, 1] * scale_y
        new_boxes = new_boxes.tolist()
    
    return new_img, new_boxes
        

'''
Giả sử mình có 1 tập các sub-module rồi, làm sao để lắp chúng vào mô đun to ?
Tên và địa chỉ 
Template 1:
Tên -> Địa chỉ 
'''
        
class SubModule:
    def __init__(self, size=(200, 200), canvas=None, samples_data=None):
        self.canvas = canvas if canvas is not None else np.ones(size)
        self.texts = []
        self.samples_data = samples_data
        self.marker_prob = 0.5 #can be change
        self.in_module_position = (0, 0)

    def get_shape(self):
        return self.canvas.shape[:2]
        
    def __paste__(self, text:str, postion:list, label:str, font_size:int, font_type:str, color:list):
        '''
        Paste single text in canvas and get its info --> overide it
        '''
        ## Draw text onto self.canvas 

        ## And append info into self.texts
    
    def __call__(self, texts):
        '''
        Paste entire text file --> overide it
        '''
        # Random if it has marker or not: 
        if np.random.random() < self.marker_prob:
            # Do some thing here
            pass
    
    def resize(self, new_shape):
        boxes = [text['box'] for text in self.texts]
        self.canvas, boxes = resize(new_shape, self.canvas, boxes)
        for i in range(len(boxes)):
            self.texts[i]['box'] = boxes[i]
        self.shape = self.canvas.shape[:2]
    
    def get_part(self, x, y):
        '''
            Get a part of canvas within (0, x) and (0, y) 
        '''
        canvas = self.canvas[:y, :x]
        texts = []
        boxes = [text['box'] for text in self.texts]
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            if x2 < x and y2 < y: # Remove box outside of the ROI
                texts.append(self.texts[i])
        part_submodule = SubModule(canvas=canvas)
        part_submodule.texts = texts
        return part_submodule

class Module:
    def __init__(self, size=(600, 600), canvas=None):
        self.canvas = canvas if canvas is not None else np.ones(size + (3,))
        self.submodules = []

    def get_shape(self):
        return self.canvas.shape[:2]

    def __paste__(self, submodule:SubModule, position:list):
        '''
            Draw submodule onto module at position where shall be topleft of submodule_box
        '''
        submodule_shape = submodule.get_shape()
        module_shape = self.get_shape()
        x, y = position #top-left
        # Check if position out of module
        assert 0 <= x < module_shape[1], "x axis of position out of bound"
        assert 0 <= y < module_shape[0], "y axis of position out of bound"
        x2 = min(x + submodule_shape[1], module_shape[1])
        y2 = min(y + submodule_shape[0], module_shape[0])

        # If submodule has bigger than x or y or both axis of module
        # We have 2 option: Resize submodule or paste a part of submodule
        if x + submodule_shape[1] > module_shape[1] or y + submodule_shape[0] < module_shape[0]:
            if np.random.random() < 0.5:      #Resize
                submodule.resize((x2-x, y2-y))
            else:       #Get part
                submodule = submodule.get_part(x2, y2)               
        
        # Paste submodule and correct the box coordinate
        self.canvas[y:y2, x:x2] = submodule.canvas
        boxes = [text['box'] for text in submodule.texts]
        boxes = mapping(boxes, position)
        for i in range(len(boxes)):
            submodule.texts[i]['box'] = boxes[i]
        submodule.in_module_position = position
        self.submodules.append(submodule)
    
    def __call__(self, submodules:list):
        '''
        Paste all submodules to modulê
        '''

    def resize(self, new_shape):
        boxes = [text['box'] for text in self.texts]
        self.canvas, boxes = resize(new_shape, self.canvas, boxes)
        for i in range(len(boxes)):
            self.texts[i]['box'] = boxes[i]
        self.shape = self.canvas.shape[:2]

    def get_part(self, x, y):
        '''
            Get a part of canvas within (0, x) and (0, y) 
        '''
        canvas = self.canvas[:y, :x]
        texts = []
        boxes = [text['box'] for text in self.texts]
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            if x2 < x and y2 < y: # Remove box outside of the ROI
                texts.append(self.texts[i])
        part_submodule = SubModule(canvas=canvas)
        part_submodule.texts = texts
        return part_submodule

# ## Below is examples

# class Seller(Module):
#     def __init__(self, size=(600, 600), canvas=None):
#         super().__init__(size, canvas)
    
#     def __call__(self, company_name, company_address, phone, fax, tax,
#                  account_number, represented_name, represented_position,
#                  account_name, bank_name, swift_code):
#         '''
#         Should list all submodule may appear in module for not be missed
#         '''
#         # We already knew that company name and company address always on top
#         # assume
