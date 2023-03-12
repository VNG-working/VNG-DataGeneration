import sys
sys.path.insert(1, r'C:\Users\chien\VNG-DataGeneration')

from gen_data import *
from common import *
from content import content
import cv2

makers_list = [
    'Add',
    'Address',
    'A/D',
    'A/d',
    'ADD',
    'ADDRESS'
]

lst_content = content['vn_unsign_add']

class Company_Address(SubModule):
    def __init__(self, shape=None, canvas=None, marker_prob=1, down_prob=0.2, marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, markers=makers_list, content=lst_content, label='company_address', ink=None):
        super().__init__(shape, canvas, marker_prob, down_prob, marker_font, content_font, markers, content, label, ink)

class Bank_Address(SubModule):
    def __init__(self, shape=None, canvas=None, marker_prob=1, down_prob=0.2, marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, markers=makers_list, content=lst_content, label='bank_address', ink=None):
        super().__init__(shape, canvas, marker_prob, down_prob, marker_font, content_font, markers, content, label, ink)