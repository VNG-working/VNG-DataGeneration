from ...gen_data import SubModule
from common import *
from content import content
from faker import Faker
from faker.providers import bank

faker = Faker()
faker.add_provider(bank)
ls_markers = [
    'bank swift code',
    'swift code',
    'swift',
    'bank\'s swift code',
]

class SwiftCode(SubModule):
    def __init__(self, shape=..., canvas=None, 
                 marker_prob=1, 
                 marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, 
                 markers=ls_markers, 
                 content=None, 
                 label='bank_name', 
                 ink=None):
        super().__init__(shape, canvas, marker_prob, marker_font, content_font, markers, content, label, ink)
        random_code = faker.swift() if np.random.rand() < 0.9 else faker.swift(length=11, primary=True)
        content = [random_code]
