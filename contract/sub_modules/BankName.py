from ...gen_data import SubModule
from common import *
from content import content

ls_markers = [
    'bank name',
    'bank\'s name',
    'beneficiary bank name',
    'beneficiary bank\'s name',
    'beneficiary banker\'s name',
    'beneficiary\'s bank',
    'at the bank',
    'bank'
]

ls_content = content["bank_name"]

class BankName(SubModule):
    def __init__(self, shape=..., canvas=None, 
                 marker_prob=1, 
                 marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, 
                 markers=ls_markers, 
                 content=ls_content, 
                 label='bank_name', 
                 ink=None):
        super().__init__(shape, canvas, marker_prob, marker_font, content_font, markers, content, label, ink)