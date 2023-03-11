import os, sys
sys.path.append(os.getcwd())
import numpy as np
from random import randint

from gen_data import *
from khoivschien.sp_func import *

import cv2 as cv

class Contract_Name(SubModule):
    def __init__(self, 
                 size = (100, 1000), 
                 canvas = None, 
                 samples_data = None,
                 font = None,
                 ink = None,
                 cursor = None,
                 font_size = None):
        super().__init__(size, canvas, samples_data)

        if canvas == None:
            self.canvas = np.uint8(np.ones(shape=(size[0], size[1], 3))*255)
        
        self.ink = ink
        self.cursor = cursor
        self.font_size = font_size
        if self.font_size != None:
            font.size = self.font_size
            self.font = font
        else:
            self.font = font

    def __paste__(self, text: str, postion: list, label: str, font_size: int, font_type: str, color: list):
        raise NotImplementedError()
        return super().__paste__(text, postion, label, font_size, font_type, color)
    
    def __call__(self, texts: str = None):
        if texts == None:
            texts = cty_lst[randint(0, len(cty_lst))]

        texts = texts.split(" ")

        text, new_canvas = write(
            text = texts,  
            ink = None, 
            bold = False, 
            font = self.font, 
            cursor = self.cursor, 
            canvas = self.canvas)
        
        self.canvas = new_canvas
    

if __name__ == "__main__":
    test = Contract_Name(cursor=(100, 50), font = normal)

    test()

    print(np.unique(test.canvas))

    cv.imshow("test", test.canvas)
    cv.waitKey(0)