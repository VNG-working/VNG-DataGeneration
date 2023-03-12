import numpy as np
from SubModule import SubModule
from common import *

class Module:
    def __init__(self, shape=(600, 600), canvas=None):
        self.canvas = canvas if canvas is not None else np.full(shape + (3,), 255, np.uint8)
        self.submodules = []

    def get_shape(self):
        return self.canvas.shape[:2]
    
    def get_fields(self):
        fields = []
        for submodule in self.submodules:
            fields += list(submodule.fields)
        return fields

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
        if x + submodule_shape[1] > module_shape[1] or y + submodule_shape[0] > module_shape[0]:
            if np.random.random() < 0:      #Resize
                submodule.resize((y2-y, x2-x))
            else:       #Get part
                submodule.get_part(x2-x, y2-y)
        
        # Paste submodule and correct the box coordinate
        self.canvas[y:y2, x:x2] = submodule.canvas
        boxes = [text['box'] for text in submodule.fields]
        boxes = mapping(boxes, position)
        for i in range(len(boxes)):
            submodule.fields[i]['box'] = boxes[i]
        submodule.in_module_position = position
        self.submodules.append(submodule)
    
    def __call__(self, submodules:list):
        '''
        Paste all submodules to module
        '''

    def resize(self, new_shape):
        boxes = [text['box'] for text in self.fields]
        self.canvas, boxes = resize(new_shape, self.canvas, boxes)
        for i in range(len(boxes)):
            self.fields[i]['box'] = boxes[i]
        self.shape = self.canvas.shape[:2]