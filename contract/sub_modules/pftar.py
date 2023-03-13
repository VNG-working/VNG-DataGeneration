import cv2
import os, sys
sys.path.append(os.getcwd())
import numpy as np
from random import randint

from gen_data import SubModule
from contract.sub_modules.content import content as Content
from contract.sub_modules.font import *

import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageFilter as ImageFilter

class Phone_Fax(SubModule):
    def __init__(self, shape = (200, 1000), canvas=None, marker_prob=0.5, down_prob=0, marker_font: ImageFont.truetype = normal, 
                 content_font: ImageFont.truetype = normal, markers=["Tel"], content=None, label="phone", ink=None):
        if content is None:
            content = []
            for x in range(14):
                if np.random.random() < 0.1:
                    content.append(" ")
                elif 0.1 <= np.random.random() < 0.3:
                    content.append("-")
                else:
                    content.append(str(randint(0, 10)))
            content = ["".join(content)]
        super().__init__(shape, canvas, marker_prob, down_prob, marker_font, content_font, markers, content, label, ink)

class AccountNumber(SubModule):
    def __init__(self, shape = (200, 1000), canvas=None, marker_prob=0.5, down_prob=0, marker_font: ImageFont.truetype = normal, 
                 content_font: ImageFont.truetype = normal, markers=["Account", "A/C No"], content=None, label="phone", ink=None):
        if content is None:
            content = []
            for x in range(10):
                content.append(str(randint(0, 10)))
            content = ["".join(content)]
        super().__init__(shape, canvas, marker_prob, down_prob, marker_font, content_font, markers, content, label, ink)

class RepresentedBy(SubModule):
    def __init__(self, shape=(1000, 1000), canvas=None, marker_prob=0.5, down_prob=0.3, marker_font: ImageFont.truetype = bold, 
                 content_font: ImageFont.truetype = bold, markers=["Represented by"], content=None, label="text", ink=None):
        if content is None:
            _call = np.random.choice(["Mr.", "Mrs.", "Miss"])
            name = np.random.choice(Content["en_per_name"])
            pos = np.random.choice(Content["pos"])
            content = [f"{_call} {name.upper()} - {pos}"]

        super().__init__(shape, canvas, marker_prob, down_prob, marker_font, content_font, markers, content, label, ink)

if __name__ == "__main__":
    phone = RepresentedBy()
    phone()

    cv2.imshow("phone", phone.canvas)
    cv2.waitKey(0)