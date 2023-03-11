import os, sys
sys.path.append(os.getcwd())
from khoivschien.common import *
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageFilter as ImageFilter
from PIL import ImageEnhance
import numpy as np

def get_text_length(self, text, font: ImageFont.truetype = None) -> int:
    if font == None:
        raise Exception("font cannot be None")

    l = 0
    for i in range(len(text)):
        l += font.getsize(text[i])[0]
    return l

def write(
          text: list, 
          char_font="normal", 
          ink=None, 
          bold=False, 
          font_size=None, 
          cursor: list=None, 
          canvas: np.array = None):
    """_summary_

    Args:
        text (list): _description_
        char_font (str, optional): _description_. Defaults to "normal".
        ink (_type_, optional): _description_. Defaults to None.
        bold (bool, optional): _description_. Defaults to False.
        font_size (_type_, optional): _description_. Defaults to None.
        cursor (list, optional): _description_. Defaults to None.
        canvas (np.array, optional): _description_. Defaults to None.

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    
    if font_size == None:
            raise Exception("size cannot be None")
    if cursor == None:
            raise Exception("cursor cannot be None")
    if canvas == None:
            raise Exception("canvas cannot be None")

    if ink is None:
        if not bold:
            ink = randink()
        else:
            ink = randink(bold=True)

    font = char_font

    cursor = list(cursor)

    while cursor[0] + get_text_length(text, font) > canvas.shape[1]:
        text = text[:-1]

    base_canvas = Image.fromarray(canvas, mode="RGB")

    draw = ImageDraw(base_canvas)

    draw.text(cursor, text, font=font, fill=ink)

    return text, np.asarray(base_canvas)