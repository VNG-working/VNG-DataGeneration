from calendar import c
# from curses import raw
from hashlib import new
from os import remove
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageFilter as ImageFilter
from click import get_text_stream
import numpy as np
import glob
import time
import pandas as pd
import json
import numpy as np
import cv2
import string
import xml.etree.ElementTree as ET
from common import *
from official_id import OfficialID
import os

labels_list = []


class CMSQ_BACK(OfficialID):
    def __init__(self, dst='data/cmsq/back/'):
        super().__init__(dst)
        if not os.path.exists(dst):
            os.makedirs(dst)
        # dst = 'data/test/'
        self.dst = dst
        self.img_name = "cmsq_back_fake_{}.jpg".format(np.random.randint(665527))
        # self.img_name = "fake_test.jpg"

        self.font_scale = np.random.randint(55, 65)
        self.original_font_scale = self.font_scale
        self.stamp_ink = (255, 51, 51)

        self.left_margin = randint(45, 55)
        self.line_height, self.original_line_height = [randint(75, 85)] * 2

        self.img_width = 1980
        self.img_height = 1200  # ratio w/h = 1.6

        bg_path = np.random.choice(
            glob.glob("bg/cmsq/back/*"))
        self.image = Image.open(bg_path).resize(
            [self.img_width, self.img_height])

        self.draw = ImageDraw.Draw(self.image)

        self.cursor = [self.left_margin, 40]  # con trỏ đầu dòng
        self.line = 0

        # define cac loai font
        self.normal = ImageFont.truetype(
            "fonts/Arial/ARIAL.ttf", size=self.font_scale+randint(0, 5))
        self.hsd = ImageFont.truetype(
            "fonts/Arial/ARIAL.ttf", size=self.font_scale-20)
        self.Bold = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale-randint(5, 8))
        self.italic = ImageFont.truetype(
            "fonts/Arial/ARIALI.ttf", size=self.font_scale)
        self.Big_Bold = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale + 10)
        self.Bold_Italic = ImageFont.truetype(
            "fonts/Arial/ARIALBI.ttf", size=self.font_scale)


        self.bbs = {
            "version": "5.0.1",
            "flags": {},
            "shapes": [],
            "imagePath": self.img_name,
            "imageHeight": self.img_height,
            "imageWidth": self.img_width
        }



        self.blocks = []
        self.fields = []

        # block related
        self.xmax = 0
        self.ymax = 0
        self.xmin = 2500

        # self.ink = tuple([int(np.random.normal(80, 20))] * 4)

    def fake_BG(self):
        bg_path = np.random.choice(
            glob.glob("bg/cmsq/back/*"))
        bg = Image.open(bg_path)
        # start = time.time()
        i = np.random.randint(4)
        bg = bg.resize([self.img_width, self.img_height])

        bg = np.array(bg)  # .getdata()).reshape(bg.size[1], bg.size[0], 3)
        image = np.array(self.image)
        bg = bg * 1./255
        image = (bg * image).astype(np.uint8)

        self.image = Image.fromarray(image)

    def word_xuongdong(self, text, fields, fields_list=[], font=None, poi=False):
        """
            text = "Ba Le thi mai linh"
            fields = ["ba", "le thi mai linh"]
            fields_list = ["gender", "transfer_name"]
        """
        "For 1 line text"
        if font == None:
            font = self.normal
        outlier = text

        idx2search = 0  # idx to start to search for field
        for i, field in enumerate(fields):
            field = str(field)
            words = field.split(" ")
            # if poi:
            #     print(words)

            # A-B gộp lại làm 1 box
            if '-' in words:
                # print(words)
                indices = [i for i, x in enumerate(words) if x == "-"]
                for idx in sorted(indices, reverse=True):
                    # concat text before and after '-'
                    words[idx-1] = words[idx-1] + \
                        ' ' + '-' + ' ' + words[idx+1]
                    # remove
                    del words[idx+1]
                    del words[idx]

            if field not in text:
                continue
            else:
                # idx dau tien cuar field trong text
                start = text.index(field, idx2search)

                # prevent more than one occurences of a field in 1 line
                # import re
                # field_idx_ls = [m.start() for m in re.finditer(field, text)]
                # if len(field_idx_ls) == 1:
                #     start = field_idx_ls[0]
                # else:
                #     return -1

            # print(text.split(" "))

            end = start + len(field)  # idx cuoi cung cuar field trong text
            idx2search = start + len(field)
            # field = "ba" => outlier = "__ le thi mai linh"
            outlier = outlier[:start] + " " * len(field) + outlier[end:]

            offset = self.cursor.copy()
            # đưa top-left của text, nội dung và font của text vào => suy ra được bb của text đó
            bb_start = self.draw.textbbox(
                offset, text[:start], font)  # bb cua phan truoc field

            # bb_end = bb_start + self.get_text_length(field)
            text_bbox = self.draw.textbbox(
                (bb_start[2], self.cursor[1]), field, font)  # bb cuar field

            bb = text_bbox
            idx = 0  # char idx in words
            for word in words:
                n = len(word)
                if n == 0:
                    idx += 1
                    continue

                word_index = field.index(word, idx)
                if idx != word_index:
                    pass

                word_bb_start = self.draw.textbbox(
                    (bb[0], bb[1]), field[:word_index], font)  # bb cua phan truoc word trong field

                word_bb = self.draw.textbbox(
                    (word_bb_start[2], self.cursor[1]), word, font)  # bb cua word trong field

                # prevent loi ra le phai
                flag_loi_ra_le_phai = False
                while word_bb[2] - self.get_last_length(word, font) // 4 > self.img_width:
                    flag_loi_ra_le_phai = True
                    re_word = word
                    return re_word

                    word = " "
                    # print('word hit deleted: ', word)
                    re_word = word

                    word = " "
                    word_bb = self.draw.textbbox(
                        (word_bb_start[2], self.cursor[1]), word, font)  # bb cua word trong field

                # prevent lot xuong duoi
                if word_bb[3] - self.get_text_height(word, font) // 5 > self.img_height:
                    continue

                self.xmax = max(self.xmax, word_bb[2])
                self.xmin = min(self.xmin, word_bb[0])
                self.ymax = max(self.ymax, word_bb[3])

                # widen box
                xmin, ymin, xmax, ymax = self.widen_box(
                    word_bb[0], word_bb[1], word_bb[2], word_bb[3])
                _field = {}
                _field["xmin"] = xmin
                _field["ymin"] = ymin
                _field["xmax"] = xmax
                _field["ymax"] = ymax
                _field["type"] = fields_list[i]
                _field["text"] = u"{}".format(word)
                # print(_field["text"])
                # print('field type: ',fields_list[i])
                self.fields.append(_field)

                idx += len(word) + 1

                if flag_loi_ra_le_phai:
                    print('final word: ', word)
                    break

        # print('outlier: ', outlier)

        self.get_outlier_coord(outlier, text, font)

        return re_word

    def fakeMainInfo(self):
        self.col_cursor = 180

        # sinh
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] = 130 + randint(-7, 7)

        raw_text = "Sinh:"
        text = raw_text
        self.write(text, char_font=self.Bold, ink=randink(True))
        self.get_marker_coord(
            text, [raw_text], ["marker_dob"], self.Bold)
        
        # actual sinh
        self.cursor[0] += self.get_text_length(text, self.Bold) + randint(5, 70)
        self.cursor[1] += randint(-7, 7)
        date = str(randint(1, 31))
        month = str(randint(1, 13))
        year = str(randint(1000, 3000))
        date = '0' + date if len(date)==1 and np.random.rand() < 0.5 else date
        month = '0' + month if len(month)==1 and np.random.rand() < 0.5 else month
        raw_text = f'Ngày {date} tháng {month} năm {year}'
        text = raw_text
        self.write(text, self.normal)
        self.get_field_coord(text, [date, month, year], ['dob']*3, self.normal)

        # dan toc
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(90, 150)
        self.cursor[1] += randint(-7, 7)
        raw_text = 'Dân tộc:'
        text = raw_text
        self.write(text, self.Bold)
        self.get_marker_coord(text, [raw_text], ['marker_ethnic'], self.Bold)

        # actual dan toc
        self.cursor[0] += self.get_text_length(text, self.Bold) + randint(30, 150)
        self.cursor[1] += randint(-7, 7)
        raw_text = rand_ethnic()
        text = raw_text
        self.write(text, self.normal)
        self.get_field_coord(text, [raw_text], ['ethnic'], self.normal)

        # que quan
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] += self.line_height + randint(10, 20)
        raw_text = "Quê quán:"
        text = raw_text
        self.write(text, char_font=self.Bold, ink=randink(True))
        self.get_marker_coord(
            text, [raw_text], ["marker_hometown"], self.Bold)

        # part 1
        self.cursor[0] = 900 + randint(-300, 300)
        self.cursor[1] += randint(-7, 7)
        raw_text = self.ward + ','
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_field_coord(text, [raw_text], ["hometown"], self.normal)
        
        # que quan part 2
        center_x = self.cursor[0] + self.get_text_length(text, self.normal) // 2
        raw_text = f"{self.district}, {self.province}."
        text = raw_text
        self.cursor[0] = center_x - self.get_text_length(text, self.normal) // 2
        self.cursor[1] += self.line_height + randint(-7, 7)
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_field_coord(text, [raw_text], ["hometown"], self.normal)


        # noi thuong tru
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] += self.line_height + randint(15, 40)
        raw_text = "Nơi thường trú:"
        text = raw_text
        self.write(text, char_font=self.Bold, ink=randink(True))
        self.get_marker_coord(
            text, [raw_text], ["marker_address"], self.Bold)

        # actual noi thuong tru
        address = np.random.choice(self.usual_addresses)
        idx = randint(2*len(address)//3, len(address))
        while address[idx] != ' ':
            idx -= 1
        part1 = address[:idx]
        part2 = address[idx+1:]

        # part 1
        self.cursor[0] += self.get_text_length(text, self.Bold) + randint(3, 70)
        self.cursor[1] += randint(-7, 7)
        raw_text = part1
        text = raw_text
        self.write(text, self.normal)
        self.get_field_coord(text, [raw_text], ['address'], self.normal)

        # part 2
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] += self.line_height + randint(-7, 7)
        raw_text = part2
        text = raw_text
        self.write(text, self.normal)
        self.get_field_coord(text, [raw_text], ['address'], self.normal)

        
        # nhan dang
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] += 5*self.line_height//2 - 20 + randint(-10, 10)
        raw_text = 'Nhân dạng:'
        text = raw_text
        self.write(text, self.Bold)
        self.get_marker_coord(text, [raw_text], ['marker_characteristic'], self.Bold)

        # actual nhan dang
        part1 = f'Cao {randint(1, 10)}m{randint(10, 100)}' + np.random.choice(['', ','])
        if np.random.rand() < 0.7:
            part2 = np.random.choice([
                "Nốt ruồi nhỏ chính giữa tai dưới",
                "Nốt ruồi nhỏ chính giữa vành môi bên phải",
                f"Nốt ruồi cách {randint(1, 100)}cm trên sau cánh mũi phải",
                f"Sẹo chấm cách {randint(1, 100)}cm trên sau cánh mũi trái",
                f"Sẹo chấm cách {randint(1, 100)}cm dưới môi phải",
                f"Sẹo chấm cách {randint(1, 100)}cm trên sau đuôi mắt trái",
            ])
        else:
            part2 = random_vn_sentences()
        
        if np.random.rand() < 0.5: # cao 1m7 dong tren, dac diem dong duoi
            # dong 1
            self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 150)
            raw_text = part1
            text = raw_text
            self.write(text, self.normal)
            self.get_field_coord(text, [raw_text], ['characteristic'], self.normal)

            # dong 2
            self.cursor[0] = self.col_cursor + randint(-30, 30)
            self.cursor[1] += self.line_height + randint(-7, 7)
            raw_text = part2
            text = raw_text
            self.write(text, self.normal)
            self.get_field_coord(text, [raw_text], ['characteristic'], self.normal)
        
        else:  # random
            characteristic = part1 + ' ' + part2
            if np.random.rand() < 0.5 or len(characteristic) > 32:  # split 2 dong
                idx = randint(2*len(characteristic)//3, len(characteristic))
                while idx >= 0:
                    if characteristic[idx] != ' ':
                        idx -= 1
                    else:
                        break

                part1 = characteristic[:idx]
                part2 = characteristic[idx+1:]

                # characteristic part 1 
                self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 100)
                raw_text = part1
                text = raw_text
                self.write(text, self.normal)
                self.get_field_coord(text, [raw_text], ['characteristic'], self.normal)

                # characteristic part 2
                self.cursor[0] = self.col_cursor + randint(-30, 30)
                self.cursor[1] += self.line_height + randint(-7, 7)
                raw_text = part2
                text = raw_text
                self.write(text, self.normal)
                self.get_field_coord(text, [raw_text], ['characteristic'], self.normal)

            else: # tren 1 dong
                self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 100)
                raw_text = characteristic
                text = raw_text
                self.write(text, self.normal)
                self.get_field_coord(text, [raw_text], ['characteristic'], self.normal)
        

        # nhom mau
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] += 5*self.line_height//2 - 20 + randint(-7, 7)
        raw_text = 'Nhóm máu:'
        text = raw_text
        self.write(text, self.Bold)
        self.get_marker_coord(text, [raw_text], ['marker_blood'], self.Bold)

        # actual nhom mau
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(10, 150)
        raw_text = np.random.choice([
            "A","B","O","AB",
        ] + list(string.ascii_uppercase)) + np.random.choice(["+", "-", ''])
        text = raw_text
        self.write(text, self.Bold)
        self.get_field_coord(text, [raw_text], ['blood'], self.Bold)
        


    def fake_glare(self):
        if np.random.rand() > 0.7:
            i = np.random.randint(0, 4)
            for _ in range(i):
                glare_path = np.random.choice(
                    glob.glob('flare/cmsq_back.png'))
                glare_img = Image.open(glare_path).resize((800, 800))
                self.image = self.image.convert("RGBA")
                glare_img = glare_img.convert("RGBA")
                # random position
                position = (np.random.randint(0, self.img_width - 800),
                            np.random.randint(0, self.img_height - 800))
                self.image.paste(glare_img, position, glare_img)
                self.image = self.image.convert("RGB")
                self.draw = ImageDraw.Draw(self.image)

    def fake_potrait(self):
        offset_x = np.random.randint(-10, 10)
        offset_y = np.random.randint(-3, 2)
        self.cursor = [158 + offset_x, 420 + offset_y]

        poitrait_path = np.random.choice(
            glob.glob('potrait/*'))
        poitrait_img = Image.open(poitrait_path).resize((420, 600))
        self.image = self.image.convert("RGBA")
        poitrait_img = poitrait_img.convert("RGBA")
        # random position
        position = tuple(self.cursor)
        self.image.paste(poitrait_img, position, poitrait_img)
        self.image = self.image.convert("RGB")
        self.draw = ImageDraw.Draw(self.image)
        print("pasted potrait")


    


    def fake(self):
        self.fakeMainInfo()
        if np.random.rand() < 0.4:
            self.fake_BG()
        self.fake_glare()
        self.fake_blur()
        self.fake_general_image()
        
        if np.random.rand() < 0.3:
            self.vien_trang()
        if np.random.rand() < 0.3:
            self.ep_plastic()
            
        self.save()


if __name__ == '__main__':
    i = 0
    while i < 1000:
        print("_______________________________________________________________________________________________________________")
        try:

            faker = CMSQ_BACK()
            print(faker.characters)
            faker.fake()
            print(faker.img_name)
            print("faking")
            i += 1

        except Exception as e:
            # raise e

            print(e)
            continue
            break
