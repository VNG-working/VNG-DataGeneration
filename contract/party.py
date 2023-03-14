import sys
import os
sys.path.append(os.getcwd())
from sub_modules.sub_modules import *
from Module import Module
import numpy as np

'''
All submodule: company_name, company_address, phone, fax, tax, 
reprenented_name, represented_position, bank_name, bank_address, account_number,
account_name, swift_code 
'''

class Party(Module):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def update_cursor(cursor, submodule, direction='down'):
        h, w = submodule.get_shape()
        if direction == 'down':
            # cursor[0] = cursor[0] #max(2, cursor[0] + randint(-5, 5))
            cursor[1] = cursor[1] + h + randint(5, 20) #x1, y2
        elif direction == 'reset_down':
            cursor[0] = 10 #randint(5, 15)
            cursor[1] = cursor[1] + h + randint(5, 20) #x1, y2
        else:
            cursor[0] = cursor[0] + w + randint(20, 100)
            # cursor[1] = cursor[1] #max(cursor[1] + randint(-5, 5), 2) #x2, y1
        return cursor
        
    def __call__(self, company_name, company_address, phone, fax, tax, reprenented_name,
                represented_position, bank_name, bank_address, account_number,
                account_name, swift_code):
            
        right_flag = False
        #Paste company name and company_address_first
        cursor = [10, 10] # x1, y1, x2, y2
        self.__paste__(company_name, position=cursor)
        cursor = self.update_cursor(cursor, company_name, 'down')

        self.__paste__(company_address, position=cursor)
        cursor = self.update_cursor(cursor, company_address, 'down')

        list_submodules = [phone, fax, tax, reprenented_name, represented_position]
        np.random.shuffle(list_submodules)
        
        #other info of company
        for i, submodule in enumerate(list_submodules):
            if np.random.random() < 0.2: # skip component
                continue
    
            self.__paste__(submodule, position=cursor)
            # print('Cursor before: ', cursor)
            if right_flag: #next component must be down line
                cursor = self.update_cursor(cursor, submodule, 'reset_down')
                right_flag = False
            else:
                if np.random.random() < 0.7: # Still downline
                    cursor = self.update_cursor(cursor, submodule, 'down')
                    right_flag = False
                else:
                    cursor = self.update_cursor(cursor, submodule, 'right')
                    right_flag = True
            # print('Cursor After: ', cursor)
        
        # Bank info
        # Random prob appear bank info
        if np.random.random() < 0.8:
            right_flag = False
            self.__paste__(bank_name, position=cursor)
            cursor = self.update_cursor(cursor, bank_name, 'down')
            
            self.__paste__(bank_address, position=cursor)
            cursor = self.update_cursor(cursor, bank_address, 'down')
            
            list_bank_modules = [account_number, account_name, swift_code]
            for submodule in list_bank_modules:
                if np.random.random() < 0.2: # skip component
                    continue
        
                self.__paste__(submodule, position=cursor)
                cursor = self.update_cursor(cursor, submodule, 'down')
    
        ## Draw now
        max_box = np.max([sub['box'] for sub in self.submodules], 0)
        xmax, ymax = max_box[2] + 5, max_box[3] + 5
        self.canvas = np.full((ymax, xmax, 3), 255, dtype=np.uint8)
        for i, sub in enumerate(self.submodules):
            x1, y1, x2, y2 = sub['box']
            self.canvas[y1:y2, x1:x2] = sub['submodule'].canvas
            
def init_party(font_size):
    font = Font(font_scale=font_size)
    font_normal, font_bold, font_italic = font.get_font('normal'), font.get_font('bold'), font.get_font('italic')
    def rand_font():
        return np.random.choice([font_normal, font_bold, font_italic])

    company_name = CompanyName(rand_font(), rand_font(), marker_prob=0.7, down_prob=0.2)()
    company_address = Company_Address(rand_font(), rand_font(),marker_prob=0.7, down_prob=0.2)()
    phone = Phone(rand_font(), rand_font(),marker_prob=1, down_prob = 0)()
    fax = Fax(rand_font(), rand_font(),marker_prob=1, down_prob = 0)()
    tax = Tax(rand_font(), rand_font(),marker_prob=1, down_prob = 0)()
    reprenented_name = RepresentedBy(rand_font(), rand_font(), marker_prob=0.8, down_prob=0.0)()
    represented_position = RepresentedPosition(rand_font(), rand_font(), marker_prob=0.3, down_prob=0.0)()
    bank_name = BankName(rand_font(), rand_font(),marker_prob=0.7, down_prob=0)()
    bank_address = Bank_Address(rand_font(), rand_font(),marker_prob=0.7, down_prob=0.2)()
    account_number = AccountNumber(rand_font(), rand_font(), marker_prob=1)()
    account_name = AccountName(rand_font(), rand_font(), marker_prob=0.7, down_prob=0.2)()
    swift_code = SwiftCode(rand_font(), rand_font(), marker_prob=1, down_prob=0)()
    
    party = Party()
    party(company_name, company_address, phone, fax, tax, reprenented_name,
            represented_position, bank_name, bank_address, account_number,
            account_name, swift_code)
    
    return party

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