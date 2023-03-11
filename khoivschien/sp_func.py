import os, sys
sys.path.append(os.getcwd())
from khoivschien.common import *
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageFilter as ImageFilter
from PIL import ImageEnhance
import numpy as np

font_scale = 32

source_txt = os.getcwd() + "/ds_cty.txt"
with open(source_txt, "r", encoding="utf-8") as f:
    lines = f.readlines()
    cty_lst = [x[:-1] for x in lines if "CÔNG TY" in x and "Mã số thuế" not in x]
    dc_lst = [" ".join(x[:-1].split(":")[-1].replace(",", " ").split(" ")) for x in lines if "Địa chỉ" in x]

normal = ImageFont.truetype(
    os.getcwd() + "/fonts/Arial/ARIAL.ttf", size=font_scale)

# hsd = ImageFont.truetype(
#     "fonts/Arial/ARIAL.ttf", size=font_scale-20)
# bold = ImageFont.truetype(
#     "fonts/Arial/ARIALBD.ttf", size=font_scale+randint(-5, 5))
# italic = ImageFont.truetype(
#     "fonts/Arial/ARIALI.ttf", size=font_scale-10)
# big_bold = ImageFont.truetype(
#     "fonts/Arial/ARIALBD.ttf", size=font_scale + 10)
# Bold_Italic = ImageFont.truetype(
#     "fonts/Arial/ARIALBI.ttf", size=font_scale)
# code_font = ImageFont.truetype(
#     "fonts/Arial/ARIAL.ttf", size=font_scale + 20)

# roboto = ImageFont.truetype('fonts/Roboto-Bold.ttf', font_scale + randint(-5, 5))
# inhoa_1 = np.random.choice([
#     ImageFont.truetype('fonts/KGNoRegretsSolid.ttf',
#                         font_scale+5),
#     ImageFont.truetype(
#         'fonts/Hand Scribble Sketch Times.otf', font_scale+5)
# ])

# bsx_font = ImageFont.truetype(
#     'fonts/Hand Scribble Sketch Times.otf', int(font_scale*2.5))
# bsx_font_small = ImageFont.truetype(
#     'fonts/Hand Scribble Sketch Times.otf', font_scale+5)

# inhoa_2 = np.random.choice([
#     ImageFont.truetype(
#         'fonts/SourceSerifPro-Semibold.otf', font_scale+5),
#     ImageFont.truetype(
#         'fonts/DroidSerif-Regular.ttf', font_scale+5),
#     ImageFont.truetype(
#         'fonts/Times-New-Roman-Bold_44652.ttf', font_scale+5),
# ])

def get_text_length(text, font: ImageFont.truetype = None) -> int:
    if font == None:
        raise Exception("font cannot be None")

    l = 0
    for i in range(len(text)):
        l += font.getsize(text[i])[0]
    return l

def write(
          text: list, 
          font: ImageFont.truetype, 
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

    Returns:
        _type_: _description_
    """

    if cursor == None:
            raise Exception("cursor cannot be None")
    if canvas.all() == None:
            raise Exception("canvas cannot be None")

    if ink is None:
        if not bold:
            ink = randink()
        else:
            ink = randink(bold=True)

    cursor = list(cursor)

    while cursor[0] + get_text_length(text = text, font = font) > canvas.shape[1]:
        text = text[:-1]

    base_canvas = Image.fromarray(canvas)

    draw = ImageDraw.Draw(base_canvas)

    draw.text(cursor, " ".join(text), font=font, fill=ink)

    return text, np.asarray(base_canvas)