import sys
import os
sys.path.append(os.getcwd())

from SubModule import SubModule
from common import *
from contract.sub_modules.content import content as all_content
from contract.sub_modules.font import *

SHAPE = (1000, 1000)

######################
### Phần của Chiến 
######################
address_markers = [
    'Add',
    'Address',
    'A/D',
    'A/d',
    'ADD',
    'ADDRESS'
]

address_content = all_content['vn_unsign_add'] + all_content['en_com_add']

comname_markers = [
    'Company Name',
    'THE SELLER',
    'THE BUYER',
    'PARTY A',
    'PARTY B',
    'SELLER',
    'BUYER'
]

comname_content = all_content['vn_com_name'] + all_content["en_com_name_abrre"]

class CompanyName(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=0.7, down_prob=0.2, ink=None):
        markers=comname_markers
        content=comname_content
        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font, markers, content, 'company_name', ink)

class Company_Address(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=0.7, down_prob=0.2,  ink=None):
        markers=address_markers
        content=address_content
        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font, markers, content, 'company_address', ink)

class Bank_Address(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=0.7, down_prob=0.2,  ink=None):
        markers=address_markers
        content=address_content
        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font, markers, content, 'bank_address', ink)

######################
### Phần của Khôi
######################

class Phone(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=0.5, down_prob = 0, ink=None):
        content = '' if np.random.random() < 0.5 else '+'
        for i in range(14):
            prob = np.random.random()
            if prob < 0.1: content += ' '
            elif 0.1 <= prob < 0.2: content += '-'
            elif 0.2 <= prob < 0.3: content += '('
            elif 0.3 <= prob < 0.4: content += ')'
            else:
                content += str(randint(0, 10))

        content = ["".join(content)]
        markers = ['Tel', 'Tel No', 'Tel Number', 'Telephone', 'Phone/ Điện thoại', 'Phone', 'City Tel', 'Mobile']
        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font,
         markers, content, 'phone', ink)

class Fax(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=0.5, down_prob = 0, ink=None):
        content = '' if np.random.random() < 0.5 else '+'
        for i in range(14):
            prob = np.random.random()
            if prob < 0.1: content += ' '
            elif 0.1 <= prob < 0.2: content += '-'
            elif 0.2 <= prob < 0.3: content += '('
            elif 0.3 <= prob < 0.4: content += ')'
            else:
                content += str(randint(0, 10))

        content = ["".join(content)]
        markers = ['Fax', 'Fax No']
        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font,
         markers, content, 'fax', ink)

class Tax(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=0.5, down_prob = 0, ink=None):    
        content = [random_number(10)]
        markers = ['Tax', 'Tax code']
        
        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font,
         markers, content, 'tax', ink)

class AccountNumber(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=0.5, down_prob = 0, ink=None):
        
        markers=["Account", "A/C No"]
       
        content = [random_number(10)]
        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font, markers, content, 'account_number', ink)

class RepresentedBy(SubModule):

    def __init__(self, marker_font, content_font, marker_prob=0.5, down_prob=0.0, ink=None):
        
        markers=["Represented by", 'Represented', 'Presented', 'Presented By']

        _call = np.random.choice(["Mr.", "Mrs.", "Miss"])
        name = np.random.choice(all_content["en_per_name"])
        pos = np.random.choice(all_content["pos"])
        content = [f"{_call} {name.upper()} - {pos}"]

        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font, markers, content, 'reprented_name', ink)

######################
### Phần của Tùng
######################
from faker import Faker
from faker.providers import bank

faker = Faker()
faker.add_provider(bank)

class SwiftCode(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=1, down_prob=0.2, ink=None):
        markers = [
            'swift code',
            'swift',
        ]

        random_code = faker.swift() if np.random.rand() < 0.9 else faker.swift(length=11, primary=True)
        content = [random_code]
        
        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font, markers, content, 'swift_code', ink)
   
class AccountName(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=0.5, down_prob=0.2, ink=None):

        
        markers = [
            'account name',
            'beneficiary',
            'beneficiary\'s name',
            'beneficiary\'s account name',
        ]
        content = all_content["en_com_name_abrre"] + all_content['vn_com_name']

        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font, markers, content, 'account_name', ink)

class BankName(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=1, down_prob=0.2, ink=None):

        markers = [
            'bank name',
            'bank\'s name',
            'beneficiary bank name',
            'beneficiary bank\'s name',
            'beneficiary banker\'s name',
            'beneficiary\'s bank',
            'at the bank',
            'bank'
        ]

        content = all_content['en_bank_name'] if marker_prob > 0 or np.random.rand() < 0.5 else ['at' + el for el in all_content['en_bank_name']]

        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font, markers, content, 'bank_name', ink)

class RepresentedPosition(SubModule):
    def __init__(self, marker_font, content_font, marker_prob=0.5, down_prob=0, ink=None):

        markers = [
            "Position",
            "Represented Position",
            "Represented by",
            "Represented",
            "Represented",
            "Representative",
            "Representator"
        ]
        content = all_content['pos']

        super().__init__(SHAPE, marker_prob, down_prob, marker_font, content_font, markers, content, 'represented_position', ink)

