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
import random
import cv2
import string
import xml.etree.ElementTree as ET
from common import *
from official_id import OfficialID
import os
labels_list = []


class SHND(OfficialID):
    def __init__(self, dst='data/shnd/first/', bg_path=None, font_dir = None):
        super().__init__(dst)
        # dst = 'data/test/'
        self.dst = dst
        self.img_name = "shnd_first_fake_{}.jpg".format(np.random.randint(665527))
        # self.img_name = "fake_test.jpg"

        self.font_scale = np.random.randint(32, 35)
        self.original_font_scale = self.font_scale
        self.stamp_ink = (255, 51, 51)

        self.left_margin = randint(45, 55)
        self.line_height, self.original_line_height = [randint(65, 75)] * 2

        self.img_width = 1485
        self.img_height = 1872  # ratio w/h = ...

        self.bg_path = bg_path
        self.image = Image.open(self.bg_path).resize([self.img_width, self.img_height])

        self.draw = ImageDraw.Draw(self.image)

        print(os.path.exists(self.dst))
        print(os.path.exists(self.bg_path))
        print(type(self.image))
        print(self.image.size)

        self.cursor = [self.left_margin, 40]  # con trỏ đầu dòng
        self.line = 0

        # define cac loai font
        self.normal = ImageFont.truetype(
            "fonts/Arial/ARIAL.ttf", size=self.font_scale)
        self.hsd = ImageFont.truetype(
            "fonts/Arial/ARIAL.ttf", size=self.font_scale-20)
        self.bold = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale+randint(-5, 5))
        self.italic = ImageFont.truetype(
            "fonts/Arial/ARIALI.ttf", size=self.font_scale-10)
        self.big_bold = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale + 10)
        self.Bold_Italic = ImageFont.truetype(
            "fonts/Arial/ARIALBI.ttf", size=self.font_scale)
        self.code_font = ImageFont.truetype(
            "fonts/Arial/ARIAL.ttf", size=self.font_scale + 20)

        self.roboto = ImageFont.truetype('fonts/Roboto-Bold.ttf', self.font_scale + randint(-5, 5))
        self.inhoa_1 = np.random.choice([
            ImageFont.truetype('fonts/KGNoRegretsSolid.ttf',
                               self.font_scale+5),
            ImageFont.truetype(
                'fonts/Hand Scribble Sketch Times.otf', self.font_scale+5)
        ])

        self.bsx_font = ImageFont.truetype(
            'fonts/Hand Scribble Sketch Times.otf', int(self.font_scale*2.5))
        self.bsx_font_small = ImageFont.truetype(
            'fonts/Hand Scribble Sketch Times.otf', self.font_scale+5)

        self.inhoa_2 = np.random.choice([
            ImageFont.truetype(
                'fonts/SourceSerifPro-Semibold.otf', self.font_scale+5),
            ImageFont.truetype(
                'fonts/DroidSerif-Regular.ttf', self.font_scale+5),
            ImageFont.truetype(
                'fonts/Times-New-Roman-Bold_44652.ttf', self.font_scale+5),
        ])

        chuki_condau_font_path = np.random.choice(glob.glob('fonts/VNI/*'))
        chuki_condau_font_path = 'fonts/VNI/UTM Zirkon.ttf'
        if chuki_condau_font_path == 'fonts/VNI/UTM Zirkon.ttf':
            self.chuki_condau_font = ImageFont.truetype(
                chuki_condau_font_path, int(self.font_scale*2.7))
        else:
            self.chuki_condau_font = ImageFont.truetype(
                chuki_condau_font_path, int(self.font_scale*1.7))

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

    def fakeMainInfo(self):
        # ho ten
        self.col_cursor = randint(300, 310)
        # if self.col_cursor < self.br_poitrait[0]:
        #     self.col_cursor = self.br_poitrait[0]+randint(50, 150)
        self.cursor[0] = self.col_cursor ++ randint(-30, 30)
        self.mark = self.cursor[0]
        self.cursor[1] += randint(1000, 1010)
        self.mapping = {0 : "Ông:", 1 : "Bà:"}
        raw_text = self.mapping[randint(0,2)]
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        # actual ho ten
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        name = np.random.choice(self.names)
        raw_text = name
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        field_lst = raw_text.split(" ")
        self.get_field_coord(text, field_lst, ["name" for i in range(len(field_lst))], self.bold)

        #ngay sinh
        self.cursor[0] = self.mark
        self.cursor[1] += self.line_height - randint(20, 30)
        raw_text = "Năm sinh:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        field_lst = raw_text.split(" ")
        self.get_marker_coord(text, field_lst, ["text" for i in range(2)], self.normal)

        # actual ngay sinh
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        raw_text = random_date().split("/")[-1]
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ["dob"], self.bold)

        # CMND
        self.cursor[0] += randint(70, 90)
        raw_text = "CMND số:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, raw_text.split(" "), ["text" for i in range(2)], self.normal)

        # actual CMND
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        raw_text = self.id
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ["id_number"], self.bold)

        # Usal Address
        self.cursor[0] = self.mark
        self.cursor[1] += self.line_height - randint(20, 30)
        raw_text = "Địa chỉ thường trú:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, raw_text.split(" "), ["text" for i in range(4)], self.normal)

        # Autual Usal Address
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        raw_text = f"Số {randint(0, 1000)} {self.ward_type} {self.ward} {self.district_type} {self.district} {self.province_type} {self.province}"
        text = raw_text
        self.cursor[1]
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, raw_text.split(" "), ["address" for i in range(len(raw_text.split(" ")))], self.normal)

        # Reall

        #name
        self.cursor[0] = self.mark 
        self.cursor[1] += randint(100, 110)
        raw_text = self.mapping[randint(0,2)]
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        # actual ho ten
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        name = np.random.choice(self.names)
        raw_text = name
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        field_lst = raw_text.split(" ")
        self.get_field_coord(text, field_lst, ["name" for i in range(len(field_lst))], self.bold)

        #ngay sinh
        self.cursor[0] = self.mark
        self.cursor[1] += self.line_height - randint(20, 30)
        raw_text = "Năm sinh:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        field_lst = raw_text.split(" ")
        self.get_marker_coord(text, field_lst, ["text" for i in range(2)], self.normal)

        # actual ngay sinh
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        raw_text = random_date().split("/")[-1]
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ["dob"], self.bold)

        # CMND
        self.cursor[0] += randint(70, 90)
        raw_text = "CMND số:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, raw_text.split(" "), ["text" for i in range(2)], self.normal)

        # actual CMND
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        raw_text = self.id
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ["id_number"], self.bold)

        # Usal Address
        self.cursor[0] = self.mark
        self.cursor[1] += self.line_height - randint(20, 30)
        raw_text = "Địa chỉ thường trú:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, raw_text.split(" "), ["text" for i in range(4)], self.normal)

        # Autual Usal Address
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        raw_text = f"Số {randint(0, 1000)} {self.ward_type} {self.ward} {self.district_type} {self.district} {self.province_type} {self.province}"
        text = raw_text
        self.cursor[1]
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, raw_text.split(" "), ["address" for i in range(len(raw_text.split(" ")))], self.normal)

        # Code
        self.cursor[0] = self.mark + randint(750, 780)
        self.cursor[1] = self.line_height + randint(1600, 1620)
        l1, l2 = random.choice(string.ascii_letters).upper(), random.choice(string.ascii_letters).upper()
        raw_text = f"{l1}{l2} {randint(100000, 999999)}"
        text = raw_text
        self.write(text, char_font=self.code_font, bold=True)
        self.get_marker_coord(text, raw_text.split(" "), ["lc_number" for i in range(len(raw_text.split(" ")))], self.code_font)


    def fake(self):
        # self.fake_stamp()
        # self.fake_potrait()
        self.fakeMainInfo()
        # if np.random.rand() < 0.4:
        #     self.fake_BG()
        # self.fake_glare()
        # self.fake_blur()
        # self.fake_logo()
        # self.fake_sign()

        # if np.random.rand() < 0.8:
        #     self.vien_trang()
        # if np.random.rand() < 0.3:
        #     self.ep_plastic()
            
        self.fake_general_image()

        self.save()


if __name__ == '__main__':
    i = 0
    print(os.getcwd())
    while i < 75:
        print("_______________________________________________________________________________________________________________")
        try:
            faker = SHND(dst = os.getcwd() + "\\data\\shnd\\first\\2user\\",
                bg_path = os.getcwd() + "\\bg\\shnd\\first\\page1.png",
                font_dir = os.getcwd() + "\\fonts\\Times New Roman")
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
