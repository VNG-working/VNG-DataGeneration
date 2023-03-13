import sys
import os
sys.path.append(os.getcwd())
from SubModule import SubModule
from common import *
from contract.sub_modules.font import *
from PIL import Image
from contract.sub_modules.content import content as all_content

class RepresentedPosition(SubModule):
    def __init__(self, shape=(300, 900), canvas=None, 
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
            "Position",
            "Represented Position",
            "Represented by",
            "Represented",
            "Represented",
            "Representative",
            "Representator"
        ]
        self.content = all_content['pos']
        self.marker_font = normal
        self.content_font = normal


if __name__ == '__main__':
    t = RepresentedPosition(shape=(300, 900))
    t()
    Image.fromarray(t.canvas).save('test.jpg')
    to_json('test.json', t.fields, t.canvas.shape)