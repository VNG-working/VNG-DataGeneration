from calendar import c
# from curses import raw
from hashlib import new
from os import remove
from turtle import home
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


class CMQD_Back(OfficialID):
    def __init__(self, dst='data/cmqd/back/'):
        super().__init__(dst)
        # dst = 'data/test/'
        self.dst = dst
        if not os.path.exists(dst):
            os.makedirs(dst)
        self.img_name = "cmqd_back_fake_{}.jpg".format(np.random.randint(665527))
        # self.img_name = "fake_test.jpg"

        self.font_scale = np.random.randint(60, 65)
        self.original_font_scale = self.font_scale
        self.stamp_ink = (255, 51, 51)

        self.left_margin = randint(45, 55)
        self.line_height, self.original_line_height = [randint(80, 90)] * 2

        self.img_width = 1980
        self.img_height = 1200  # ratio w/h = 1.6

        bg_path = np.random.choice(
            glob.glob("bg/cmqd/back/*"))
        self.image = Image.open(bg_path).resize(
            [self.img_width, self.img_height])

        self.draw = ImageDraw.Draw(self.image)

        self.cursor = [self.left_margin, 40]  # con trỏ đầu dòng
        self.line = 0

        # define cac loai font
        self.normal = ImageFont.truetype(
            "fonts/Arial/ARIAL.ttf", size=self.font_scale+5)
        self.hsd = ImageFont.truetype(
            "fonts/Arial/ARIAL.ttf", size=self.font_scale-20)
        self.bold = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale)
        self.italic = ImageFont.truetype(
            "fonts/Arial/ARIALI.ttf", size=self.font_scale)
        self.big_bold = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale + 10)
        self.bold_italic = ImageFont.truetype(
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
            glob.glob("bg/cmqd/back/*"))
        bg = Image.open(bg_path)
        # start = time.time()
        i = np.random.randint(4)
        bg = bg.resize([self.img_width, self.img_height])

        bg = np.array(bg)  # .getdata()).reshape(bg.size[1], bg.size[0], 3)
        image = np.array(self.image)
        bg = bg * 1./255
        image = (bg * image).astype(np.uint8)

        self.image = Image.fromarray(image)

    
    
    def fakeMainInfo(self):
        
        # que quan
        self.col_cursor = 250 + randint(-50, 50)
        self.cursor[0] = self.col_cursor + randint(-50, 50)
        self.cursor[1] = 245 + randint(-50, 50)
        raw_text = "Quê quán:"
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["marker_hometown"], self.normal)
        
        # actual que quan
        hometown = np.random.choice(self.hometown)
        if np.random.rand() < 0.4 or len(hometown) > 45:
            print(len(hometown))
            idx = randint(2*len(hometown)//3, len(hometown))
            while idx >= 0:
                if hometown[idx] != ' ':
                    idx -= 1
                else:
                    break

            part1 = hometown[:idx]
            part2 = hometown[idx+1:]

            # hometown part 1 
            self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 100)
            raw_text = part1
            text = raw_text
            self.write(text, self.bold)
            self.get_field_coord(text, [raw_text], ['hometown'], self.bold)

            # hometown part 2
            self.cursor[0] = self.col_cursor + randint(-50, 50)
            self.cursor[1] += self.line_height + randint(-10, 10)
            raw_text = part2
            text = raw_text
            self.write(text, self.bold)
            self.get_field_coord(text, [raw_text], ['hometown'], self.bold)

        else:
            print(len(hometown))
            self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 100)
            raw_text = hometown
            text = raw_text
            self.write(text, self.bold)
            self.get_field_coord(text, [raw_text], ['hometown'], self.bold)


        # noi thuong tru
        self.cursor[0] = self.col_cursor + randint(-50, 50)
        self.cursor[1] += self.line_height + randint(25, 35)
        raw_text = 'Nơi thường trú:'
        text = raw_text
        self.write(text, self.normal)
        self.get_marker_coord(text, [raw_text], ['marker_address'], self.normal)

        # actual address
        address = np.random.choice(self.usual_addresses)
        if np.random.rand() < 0.4 or len(address) > 35:
            idx = randint(2*len(address)//3, len(address))
            while idx >= 0:
                if address[idx] != ' ':
                    idx -= 1
                else:
                    break

            part1 = address[:idx]
            part2 = address[idx+1:]

            # address part 1 
            self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 100)
            raw_text = part1
            text = raw_text
            self.write(text, self.bold)
            self.get_field_coord(text, [raw_text], ['address'], self.bold)

            # address part 2
            self.cursor[0] = self.col_cursor + randint(-50, 50)
            self.cursor[1] += self.line_height + randint(-10, 10)
            raw_text = part2
            text = raw_text
            self.write(text, self.bold)
            self.get_field_coord(text, [raw_text], ['address'], self.bold)

        else:
            self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 100)
            raw_text = address
            text = raw_text
            self.write(text, self.bold)
            self.get_field_coord(text, [raw_text], ['address'], self.bold)

        # nhan dang
        self.cursor[0] = self.col_cursor + randint(-50, 50)
        self.cursor[1] += self.line_height + randint(25, 35)
        raw_text = 'Nhân dạng:'
        text = raw_text
        self.write(text, self.normal)
        self.get_marker_coord(text, [raw_text], ['marker_characteristic'], self.normal)

        # actual nhan dang
        part1 = f'Cao {randint(1, 10)}m{randint(10, 100)}, '
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
            self.write(text, self.bold)
            self.get_field_coord(text, [raw_text], ['characteristic'], self.bold)

            # dong 2
            self.cursor[0] = self.col_cursor + randint(-50, 50)
            self.cursor[1] += self.line_height + randint(-10, 10)
            raw_text = part2
            text = raw_text
            self.write(text, self.bold)
            self.get_field_coord(text, [raw_text], ['characteristic'], self.bold)
        
        else:  # random
            characteristic = part1 + ' ' + part2
            if np.random.rand() < 0.5 or len(characteristic) > 40:  # split 2 dong
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
                self.write(text, self.bold)
                self.get_field_coord(text, [raw_text], ['characteristic'], self.bold)

                # characteristic part 2
                self.cursor[0] = self.col_cursor + randint(-50, 50)
                self.cursor[1] += self.line_height + randint(-10, 10)
                raw_text = part2
                text = raw_text
                self.write(text, self.bold)
                self.get_field_coord(text, [raw_text], ['characteristic'], self.bold)

            else: # tren 1 dong
                self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 100)
                raw_text = characteristic
                text = raw_text
                self.write(text, self.bold)
                self.get_field_coord(text, [raw_text], ['characteristic'], self.bold)
            
        # nhom mau
        self.cursor[0] = self.col_cursor + randint(-50, 50)
        self.cursor[1] += self.line_height + randint(15, 25)
        raw_text = 'Nhóm máu:'
        text = raw_text
        self.write(text, self.normal)
        self.get_marker_coord(text, [raw_text], ['marker_blood'], self.normal)

        # actual nhom mau
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(50, 150)
        raw_text = np.random.choice([
            "A","B","O","AB",
        ] + list(string.ascii_uppercase)) + np.random.choice(["+", "-", ''])
        text = raw_text
        self.write(text, self.bold)
        self.get_field_coord(text, [raw_text], ['blood'], self.bold)






        
        
        

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

        glare_path = np.random.choice(
            glob.glob('potrait/*'))
        glare_img = Image.open(glare_path).resize((420, 600))
        self.image = self.image.convert("RGBA")
        glare_img = glare_img.convert("RGBA")
        # random position
        position = tuple(self.cursor)
        self.image.paste(glare_img, position, glare_img)
        self.image = self.image.convert("RGB")
        self.draw = ImageDraw.Draw(self.image)
        print("pasted potrait")

    def fake(self):
        self.fakeMainInfo()
        if np.random.rand() < 0.4:
            self.fake_BG()
        self.fake_glare()
        self.fake_blur()

        if np.random.rand() < 0.3:
            self.vien_trang()
        if np.random.rand() < 0.3:
            self.ep_plastic()
            
        self.fake_general_image()
        self.save()


if __name__ == '__main__':
    i = 0
    while i < 1000:
        print("_______________________________________________________________________________________________________________")
        try:
            faker = CMQD_Back()
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
