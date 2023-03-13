import sys
import os
sys.path.append(os.getcwd())

from SubModule import SubModule
from common import *
from contract.sub_modules.content import content as all_content
from contract.sub_modules.font import *

makers_list = [
    'Add',
    'Address',
    'A/D',
    'A/d',
    'ADD',
    'ADDRESS'
]

lst_content = all_content['vn_unsign_add'] + all_content['en_com_add']

class Company_Address(SubModule):
    def __init__(self, shape=None, canvas=None, marker_prob=1, down_prob=0.2, marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, markers=makers_list, content=lst_content, label='company_address', ink=None):
        super().__init__(shape, canvas, marker_prob, down_prob, marker_font, content_font, markers, content, label, ink)

class Bank_Address(SubModule):
    def __init__(self, shape=None, canvas=None, marker_prob=1, down_prob=0.2, marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, markers=makers_list, content=lst_content, label='bank_address', ink=None):
        super().__init__(shape, canvas, marker_prob, down_prob, marker_font, content_font, markers, content, label, ink)