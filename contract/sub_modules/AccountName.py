from ...gen_data import SubModule
from common import *
from content import content

ls_markers = [
    'account name',
    'beneficiary',
    'beneficiary\'s name',
    'beneficiary\'s account name',
]

ls_content = content["company_name"]

class AccountName(SubModule):
    def __init__(self, shape=..., canvas=None, 
                 marker_prob=0.5, 
                 marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, 
                 markers=ls_markers, 
                 content=ls_content, 
                 label='account_name', 
                 ink=None):
        super().__init__(shape, canvas, marker_prob, marker_font, content_font, markers, content, label, ink)