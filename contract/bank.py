import sys
import os
sys.path.append(os.getcwd())

from sub_modules.sub_modules import *
from Module import Module
import numpy as np

'''
    - required submodules:  bank_name; company_name for "benificiary"; 
                            bank_address; account_number
    - may or may not existed submodules: fax, swift_code, reprenented_name, represented_position, phone, tax
'''

class Bank(Module):
    def __init__(self):
        super().__init__()

    @staticmethod
    def update_cursor(cursor, submodule, direction='down'):
        h, w = submodule.get_shape()
        if direction == 'down':
            cursor[0] = max(2, cursor[0] + randint(-5, 5))
            cursor[1] = cursor[1] + h + randint(5, 10) #x1, y2
        elif direction == 'reset_down':
            cursor[0] = randint(5, 15)
            cursor[1] = cursor[1] + h + randint(5, 10) #x1, y2
        else:
            cursor[0] = cursor[0] + w + randint(5, 10)
            cursor[1] =  max(cursor[1] + randint(-5, 5), 2) #x2, y1
        return cursor


    def __call__(self, company_name, company_address, phone, fax, tax, reprenented_name,
                represented_position, bank_name, bank_address, account_number,
                account_name, swift_code):

        cursor = [10, 10]

        # bank_name is always written on top
        self.__paste__(bank_name, cursor)
        cursor = self.update_cursor(cursor, bank_name)

        required_modules = [company_name, bank_address]

        hideable_modules = [account_number, fax, swift_code, 
                            reprenented_name, represented_position, phone, tax]
        
        all_modules = required_modules + hideable_modules

        small_modules = [account_name, fax, swift_code, phone, tax]

        np.random.shuffle(all_modules)

        flag_cursor, previous_module = 'down', None

        for i, submodule in enumerate(all_modules):
            # If submodule is required, paste and update cursor
            if submodule in required_modules:
                self.__paste__(submodule, cursor)
                cursor = self.update_cursor(cursor, submodule)

            # If submodule is hideable and should be pasted, paste and update cursor
            elif submodule in hideable_modules and np.random.random() < 0.8:
                if submodule in small_modules:
                    if previous_module is None or previous_module not in small_modules:
                        self.__paste__(submodule, cursor)
                        flag_cursor = 'right' if np.random.random() < 0.5 else 'reset_down'
                        cursor = self.update_cursor(cursor, submodule, direction=flag_cursor)
                    else:
                        self.__paste__(submodule, cursor)
                        cursor = self.update_cursor(cursor, submodule, direction='reset_down')
                else:
                    self.__paste__(submodule, cursor)
                    if flag_cursor == 'right' and submodule not in small_modules:
                        cursor = self.update_cursor(cursor, submodule, direction='reset_down')
                    else:
                        cursor = self.update_cursor(cursor, submodule)
            
            # Skip submodule if it shouldn't be pasted
            else:
                continue
            
            flag_cursor = 'down'
            previous_module = submodule

        # Draw now
        max_box = np.max([sub['box'] for sub in self.submodules], 0)
        xmax, ymax = max_box[2] + 5, max_box[3] + 5
        self.canvas = np.full((ymax, xmax, 3), 255, dtype=np.uint8)
        for i, sub in enumerate(self.submodules):
            x1, y1, x2, y2 = sub['box']
            self.canvas[y1:y2, x1:x2] = sub['submodule'].canvas

if __name__ == '__main__':
    import cv2
    for i in range(10):
        bank = Bank()
        company_name = CompanyName(marker_prob=0.7, down_prob=0.2)()
        company_address = Company_Address(marker_prob=0.7, down_prob=0.2)()
        phone = Phone(marker_prob=1, down_prob = 0)()
        fax = Fax(marker_prob=1, down_prob = 0)()
        tax = Tax(marker_prob=1, down_prob = 0)()
        reprenented_name = RepresentedBy(marker_prob=0.8, down_prob=0.0)()
        represented_position = RepresentedPosition(marker_prob=0.3, down_prob=0.0)()
        bank_name = BankName(marker_prob=0.7, down_prob=0)()
        bank_address = Bank_Address(marker_prob=0.7, down_prob=0.2)()
        account_number = AccountNumber(marker_prob=1, down_prob=0.0)()
        account_name = AccountName(marker_prob=0.7, down_prob=0.2)()
        swift_code = SwiftCode(marker_prob=1, down_prob=0)()
        bank(company_name, company_address, phone, fax, tax, reprenented_name,
                represented_position, bank_name, bank_address, account_number,
                account_name, swift_code)

        fields = bank.get_fields()
        for field in fields:
            x1, y1, x2, y2 = field['box']
            bank.canvas = cv2.rectangle(bank.canvas, (x1, y1), (x2, y2), (0, 255, 0), thickness = 1)

        cv2.imshow('img', bank.canvas)
        key = cv2.waitKey(0)
        if key == ord('q'):
            exit(-1)