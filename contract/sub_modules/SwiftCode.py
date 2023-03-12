import sys
import os
sys.path.append(os.getcwd())

from gen_data import SubModule
from common import *
from contract.sub_modules.font import *
from faker import Faker
from faker.providers import bank

faker = Faker()
faker.add_provider(bank)

class SwiftCode(SubModule):
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
            'bank swift code',
            'swift code',
            'swift',
            'bank\'s swift code',
        ]

        random_code = faker.swift() if np.random.rand() < 0.9 else faker.swift(length=11, primary=True)
        self.content = [random_code]

        self.marker_font = normal
        self.content_font = normal

if __name__ == '__main__':
    t = SwiftCode(shape=(300, 900))
    t()
    Image.fromarray(t.canvas).save('test.jpg')
    to_json('test.json', t.fields, t.canvas.shape)

