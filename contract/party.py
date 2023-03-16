import sys
import os
sys.path.append(os.getcwd())
from sub_modules.sub_modules import *
from Module import Module
import numpy as np
from common import *

'''
All submodule: company_name, company_address, phone, fax, tax, 
reprenented_name, bank_name, bank_address, account_number,
account_name, swift_code 
'''

class Party(Module):
    def __init__(self, skip_prob:float = 0.2, down_prob:float = 0.7, bank_prob = 0.8):
        self.skip_prob = skip_prob
        self.down_prob = down_prob
        self.bank_prob = bank_prob
        self.step_down = np.random.randint(5, 20)
        super().__init__()
    
    def update_cursor(self, cursor, submodule, direction='down'):
        h, w = submodule.get_shape()
        if direction == 'down':
            # cursor[0] = cursor[0] #max(2, cursor[0] + randint(-5, 5))
            cursor[1] = cursor[1] + h + self.step_down + np.random.randint(-2, 2) #x1, y2
        elif direction == 'reset_down':
            cursor[0] = 10 #randint(5, 15)
            cursor[1] = cursor[1] + h + self.step_down + np.random.randint(-2, 2) #x1, y2
        else:
            cursor[0] = cursor[0] + w + randint(20, 100)
            # cursor[1] = cursor[1] #max(cursor[1] + randint(-5, 5), 2) #x2, y1
        return cursor
        
    def __call__(self, company_name, company_address, phone, fax, tax, represented_name, 
                bank_name, bank_address, account_number, account_name, swift_code):
            
        right_flag = False
        #Paste company name and company_address_first
        cursor = [10, 10] # x1, y1, x2, y2
        self.__paste__(company_name, position=cursor)
        cursor = self.update_cursor(cursor, company_name, 'down')

        self.__paste__(company_address, position=cursor)
        cursor = self.update_cursor(cursor, company_address, 'down')

        list_submodules = [phone, fax, tax, represented_name]
        np.random.shuffle(list_submodules)
        
        #other info of company
        for i, submodule in enumerate(list_submodules):
            if np.random.random() < self.skip_prob: # skip component
                continue
    
            self.__paste__(submodule, position=cursor)
            if right_flag: #next component must be down line
                cursor = self.update_cursor(cursor, submodule, 'reset_down')
                right_flag = False
            else:
                if np.random.random() < self.down_prob: # Still downline
                    cursor = self.update_cursor(cursor, submodule, 'down')
                    right_flag = False
                else:
                    cursor = self.update_cursor(cursor, submodule, 'right')
                    right_flag = True
        
        # Bank info
        if np.random.random() < self.bank_prob:
            type = np.random.choice([1, 2]) if bank_name.has_marker else 2  # neu bank_name ko co marker, no phai nam cung dong voi account_name hoac nam ngay duoi
            skip_prob_dict = {
                'BankName': 0,
                'Bank_Address': 0.3,
                'AccountNumber': 0,
                'AccountName': 0.7,
                'SwiftCode': 0.3
            }
            ls_submodules = [bank_name, bank_address, account_number, account_name, swift_code]
            if type == 1: # moi field 1 dong
                if np.random.rand() < 0.2:
                    np.random.shuffle(ls_submodules)
                for submodule in ls_submodules:
                    if np.random.rand() < skip_prob_dict[submodule.__class__.__name__]:
                        continue
                    self.__paste__(submodule, position=cursor)
                    cursor = self.update_cursor(cursor, submodule, 'down')

            elif type == 2: # co the co 2 field 1 dong
                # dinh nghia cac submodule co the o cung 1 dong
                submodule_name_pair = [('AccountNumber', 'BankName'), ('AccountName', 'AccountNumber'), ('AccountNumber', 'SwiftCode')][np.random.choice([0, 1, 2], p=[0.6, 0.2, 0.2])]
                submodule_pair = [submodule for submodule in ls_submodules if submodule.__class__.__name__ in submodule_name_pair]
                if not bank_name.has_marker and bank_name != submodule_pair[1]: # neu bank_name ko co marker => no phai o sau account_number
                    submodule_pair = submodule_pair[::-1]
                else:
                    np.random.shuffle(submodule_pair)
                is_submodule_pair_pasted = False

                for submodule in ls_submodules:
                    if np.random.rand() < skip_prob_dict[submodule.__class__.__name__]:
                        continue
                    if submodule not in submodule_pair:
                        self.__paste__(submodule, position=cursor)
                        cursor = self.update_cursor(cursor, submodule, 'down')
                    else:
                        if not is_submodule_pair_pasted:
                            for i, submodule in enumerate(submodule_pair):
                                self.__paste__(submodule, position=cursor)
                                update_cursor_type = 'reset_down' if i==1 or (submodule.__class__.__name__ == 'BankName' and np.random.rand() < 0.5) else 'right'
                                cursor = self.update_cursor(cursor, submodule, update_cursor_type)
                            is_submodule_pair_pasted = True
    
        ## Draw now
        max_box = np.max([sub['box'] for sub in self.submodules], 0)
        xmax, ymax = max_box[2] + 5, max_box[3] + 5
        self.canvas = np.full((ymax, xmax, 3), 255, dtype=np.uint8)
        for i, sub in enumerate(self.submodules):
            x1, y1, x2, y2 = sub['box']
            self.canvas[y1:y2, x1:x2] = sub['submodule'].canvas
            
# def init_party(font_size):
#     font = Font(font_scale=font_size)
#     font_normal, font_bold, font_italic = font.get_font('normal'), font.get_font('bold'), font.get_font('italic')
#     def rand_font():
#         return np.random.choice([font_normal, font_bold, font_italic])

#     company_name = CompanyName(rand_font(), rand_font(), marker_prob=0.7, down_prob=0.2)()
#     company_address = Company_Address(rand_font(), rand_font(),marker_prob=0.7, down_prob=0.2)()
#     phone = Phone(rand_font(), rand_font(),marker_prob=1, down_prob = 0)()
#     fax = Fax(rand_font(), rand_font(),marker_prob=1, down_prob = 0)()
#     tax = Tax(rand_font(), rand_font(),marker_prob=1, down_prob = 0)()
#     represented_name = RepresentedBy(rand_font(), rand_font(), marker_prob=0.8, down_prob=0.0)()
#     represented_position = RepresentedPosition(rand_font(), rand_font(), marker_prob=0.3, down_prob=0.0)()
#     bank_name = BankName(rand_font(), rand_font(),marker_prob=0.7, down_prob=0)()
#     bank_address = Bank_Address(rand_font(), rand_font(),marker_prob=0.7, down_prob=0.2)()
#     account_number = AccountNumber(rand_font(), rand_font(), marker_prob=1)()
#     account_name = AccountName(rand_font(), rand_font(), marker_prob=0.7, down_prob=0.2)()
#     swift_code = SwiftCode(rand_font(), rand_font(), marker_prob=1, down_prob=0)()
    
#     party = Party()
#     party(company_name, company_address, phone, fax, tax, represented_name,
#             represented_position, bank_name, bank_address, account_number,
#             account_name, swift_code)
    
#     return party

if __name__ == '__main__':
    import cv2
    for i in range(10):
        buyer = init_party(20)
    
        fields = buyer.get_fields()
        for field in fields:
            x1, y1, x2, y2 = field['box']
            buyer.canvas = cv2.rectangle(buyer.canvas, (x1, y1), (x2, y2), (0, 255, 0), thickness = 1)

        cv2.imshow('img', buyer.canvas)
        key = cv2.waitKey(0)
        if key == ord('q'):
            exit(-1)