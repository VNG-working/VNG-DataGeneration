import sys
import os
sys.path.append(os.getcwd())

from SubModule import SubModule
from common import *
from contract.sub_modules.content import content as all_content
from contract.sub_modules.font import *



class BankName(SubModule):
    def __init__(self, shape=..., canvas=None, 
                 marker_prob=1, 
                 down_prob=0.2,
                 marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, 
                 markers=None, 
                 content=None, 
                 label='bank_name', 
                 ink=None):
        super().__init__(shape, canvas, marker_prob, down_prob, marker_font, content_font, markers, content, label, ink)

        self.markers = [
            'bank name',
            'bank\'s name',
            'beneficiary bank name',
            'beneficiary bank\'s name',
            'beneficiary banker\'s name',
            'beneficiary\'s bank',
            'at the bank',
            'bank'
        ]

        self.content = all_content['en_bank_name']
        self.marker_font = normal
        self.content_font = normal

if __name__ == '__main__':
    t = BankName(shape=(300, 900))
    t()
    Image.fromarray(t.canvas).save('test.jpg')
    to_json('test.json', t.fields, t.canvas.shape)