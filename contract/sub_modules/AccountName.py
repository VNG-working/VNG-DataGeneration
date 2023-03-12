import sys
import os
sys.path.append(os.getcwd())

from SubModule import SubModule
from common import *
from contract.sub_modules.content import content as all_content
from contract.sub_modules.font import *

print(all_content.keys())

class AccountName(SubModule):
    def __init__(self, shape=..., canvas=None, 
                 marker_prob=0.5,
                 down_prob=0.2,
                 marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, 
                 markers=None, 
                 content=None, 
                 label='account_name', 
                 ink=None):
        super().__init__(shape, canvas, marker_prob, down_prob, marker_font, content_font, markers, content, label, ink)

        self.markers = [
            'account name',
            'beneficiary',
            'beneficiary\'s name',
            'beneficiary\'s account name',
        ]
        self.content = all_content["en_com_name_abrre"] + all_content['vn_com_name']
        self.marker_font = normal
        self.content_font = normal

if __name__ == '__main__':
    t = AccountName(shape=(300, 900))
    t()
    Image.fromarray(t.canvas).save('test.jpg')
    to_json('test.json', t.fields, t.canvas.shape)