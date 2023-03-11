import os, sys
sys.path.append(os.getcwd())
import numpy as np

from gen_data import *
from khoivschien.sp_func import *

class Contract_Name(SubModule):
    def __init__(self, 
                 size = (200, 200), 
                 canvas = None, 
                 samples_data = None,
                 font = None,
                 char_font = "normal",
                 ink = None,
                 cursor = None):
        super().__init__(size, canvas, samples_data)

        if canvas == None:
            canvas = np.ones(shape=(size[0], size[1], 3))*255
            self.canvas = canvas.astype(int)
        self.font = font
        self.charfont = char_font
        self.ink = ink
        self.cursor = cursor

    def __paste__(self, text: str, postion: list, label: str, font_size: int, font_type: str, color: list):
        raise NotImplementedError()
        return super().__paste__(text, postion, label, font_size, font_type, color)
    
    def __call__(self, texts: str):
        texts = texts.split(" ")

        text, new_canvas = write(
            text = texts, 
            char_font = self.charfont, 
            ink = None, 
            bold = False, 
            font_size = None, 
            cursor = self.cursor, 
            canvas = self.canvas)
        
        self.canvas = new_canvas
    

if __name__ == "__main__":
    test = Contract_Name()