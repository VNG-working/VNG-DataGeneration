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


class SHND(OfficialID):
    def __init__(self, dst='data/shnd/first/', bg_path=None, font_dir = None):
        super().__init__(dst)
        # dst = 'data/test/'
        self.dst = dst
        # self.img_name = "shnd_first_fake_{}.jpg".format(np.random.randint(665527))
        self.img_name = "fake_test.jpg"

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

    def fake_BG(self):
        bg_path = np.random.choice(
            glob.glob("bg/cmca/front/*"))
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
        self.get_marker_coord(text, [raw_text], ["name"], self.normal)

        # actual ho ten
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        name = np.random.choice(self.names)
        raw_text = name
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ["name"], self.bold)

        #ngay sinh
        self.cursor[0] = self.mark
        self.cursor[1] += self.line_height - randint(20, 30)
        raw_text = "Năm sinh:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

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
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        # actual CMND
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        raw_text = random_date()
        text = self.id
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ["id_number"], self.bold)

        # Usal Address
        self.cursor[0] = self.mark
        self.cursor[1] += self.line_height - randint(20, 30)
        raw_text = "Địa chỉ thường trú:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        # Autual Usal Address
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(20, 30)
        raw_text = f"Số {randint(0, 1000)} {self.ward_type} {self.ward} {self.district_type} {self.district} {self.province_type} {self.province}"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

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
        offset_x = np.random.randint(-50, 50)
        offset_y = np.random.randint(-50, 50)
        self.tl_poitrait = (158 + offset_x, 420 + offset_y)

        poitrait_path = np.random.choice(glob.glob('potrait/*'))
        offset = randint(-20, 20)
        size = (400 + offset, 560 + offset)
        poitrait_img = Image.open(poitrait_path).resize(size)
        
        augment = np.random.choice([1, 2, 3])
        if augment == 1:
            poitrait_img = rounded_img(np.array(poitrait_img))
        elif augment == 2:
            poitrait_img = ep_plastic(np.array(poitrait_img))
        elif augment == 3:
            poitrait_img = vien_trang(np.array(poitrait_img))

        poitrait_img = Image.fromarray(poitrait_img).convert('RGBA')
        self.image = self.image.convert("RGBA")

        # random position
        self.image.paste(poitrait_img, self.tl_poitrait, poitrait_img)
        self.image = self.image.convert("RGB")
        self.draw = ImageDraw.Draw(self.image)
        self.br_poitrait = (self.tl_poitrait[0] + poitrait_img.size[0], self.tl_poitrait[1] + poitrait_img.size[1])


    def fake_logo(self):
        from pathlib import Path

        offset_x = np.random.randint(-50, 50)
        offset_y = np.random.randint(-50, 50)
        self.tl_poitrait = (200 + offset_x, 100 + offset_y)

        logo_path = np.random.choice(glob.glob('logo/ca*.jpg'))
        offset = randint(-20, 20)
        size = (310+offset, 310+offset)

        logo_img = Image.open(logo_path).resize(size)
        
        mask = Image.new('L', logo_img.size, 0)
        draw = ImageDraw.Draw(mask)
        if Path(logo_path).stem == 'ca':
            print('ok ok ok')
            draw.rounded_rectangle((10, 10) + (logo_img.size[0]-10, logo_img.size[1]-10), radius=120, fill=255)
        else:
            draw.rounded_rectangle((10, 10) + (logo_img.size[0]-10, logo_img.size[1]-10), radius=200, fill=255)

        logo_img.putalpha(mask)
        self.image = self.image.convert("RGBA")

        # random position
        self.image.paste(logo_img, self.tl_poitrait, logo_img)
        self.image = self.image.convert("RGB")
        self.draw = ImageDraw.Draw(self.image)
        self.br_poitrait = (self.tl_poitrait[0] + logo_img.size[0], self.tl_poitrait[1] + logo_img.size[1])


    def fake_stamp(self):
        offset_x = int(np.random.randint(-70, 70))
        offset_y = int(np.random.randint(-70, 70))

        self.stamp_area = [1000 + offset_x,  600 + offset_y, 1500 + offset_x ,  1100 + offset_y]

        stamp_path = np.random.choice(glob.glob("stamp/*.png"))

        stamp = cv2.imread(stamp_path)
        stamp = random_rotate(stamp)
        # stamp = constrast_stretching(stamp)

        self.image = self.image.convert('RGB')
        src = np.array(self.image) # current self.image
        stamp = cv2.resize(stamp , (self.stamp_area[2] - self.stamp_area[0] , self.stamp_area[3] - self.stamp_area[1])) # resize stamp
        stamp = cv2.cvtColor(stamp, cv2.COLOR_BGR2RGB) # convert to RGB
        
        # filter white pixel
        mask = np.any((stamp[:,:,1:] < 200),axis= -1)
        mask = np.expand_dims(mask , -1)

        print(mask.shape)
        print(np.unique(mask))
        stamp = mask * list(self.stamp_ink)  * np.random.randint(600, 900) / 1000.
        print(stamp.shape)

        # cho nao mask=1 thi lay cua stamp
        # cho nao mask=0 thi lay cua anh goc
        print('stamp shape', stamp.shape)
        print('mask shape: ', mask.shape)
        print('shape: ', src[self.stamp_area[1] : self.stamp_area[3] , self.stamp_area[0] : self.stamp_area[2]].shape)
        stamp = stamp * mask + src[self.stamp_area[1] : self.stamp_area[3] , self.stamp_area[0] : self.stamp_area[2]] * (1-mask) 

        # find pixel position in mask that has value = 1
        temp = np.where(mask == 1)
        pos = [temp[0][0], temp[1][0]]
        self.stamp_ink = stamp[pos[0], pos[1]]
        # convert to int
        self.stamp_sign_ink = tuple([int(x) for x in self.stamp_ink]) 

        # src[sign1_rec[1] : sign1_rec[3] , sign1_rec[0] : sign1_rec[2]] =  stamp
        stamp = Image.fromarray(stamp.astype(np.uint8)).convert('RGBA')
        # blend stamp with src
        temp = src[self.stamp_area[1] : self.stamp_area[3] , self.stamp_area[0] : self.stamp_area[2]]
        temp = Image.fromarray(temp).convert('RGBA')
        factor = rand_normal(0.7, 0.1)
        temp = Image.blend(temp, stamp, factor)
        temp = temp.convert('RGB')
        src[self.stamp_area[1] : self.stamp_area[3] , self.stamp_area[0] : self.stamp_area[2]] = np.array(temp)

        

        self.image = Image.fromarray(src)
        self.draw = ImageDraw.Draw(self.image)


    def fake_sign(self):
        # print(self.cursor)
        offset_x = int(np.random.normal(-50,50))
        offset_y = int(np.random.normal(-50,50))

        x = 1200 + offset_x
        y = 800 + offset_y
        self.sign_area = [x, y, x+600, y+300]

        self.signature_path = np.random.choice(glob.glob("new_signature/*"))
        # self.signature_path = np.random.choice(glob.glob("sign/*"))
        signal = cv2.imread(self.signature_path)
        # signal = signal > 250
        signal = random_rotate(signal , deg_range = 15 , border = (0))
        signal = constrast_stretching(signal)
        
        src = np.array(self.image)
        self.signature_mask = np.zeros_like(src)
        signal = cv2.resize(signal , (self.sign_area[2] - self.sign_area[0] , self.sign_area[3] - self.sign_area[1]))
        mask = (signal > 200).astype(np.uint8)
        
        
        inks = list([[1,1,1] , [1,0,0], [1,0,0],[1,0,0]])
        ink = inks[np.random.randint(len(inks))]
        ink = np.array(ink) * np.random.randint(100)
        # print(ink.shape)
        # ink = np.array([0, 102, 255])
        print(ink.shape)

        
        signal = mask * ink + src[self.sign_area[1] : self.sign_area[3] , self.sign_area[0] : self.sign_area[2]] * (1-mask)
        src[self.sign_area[1] : self.sign_area[3] , self.sign_area[0] : self.sign_area[2]] =  signal
        self.image = Image.fromarray(src)


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
    while i < 1:
        print("_______________________________________________________________________________________________________________")
        try:
            faker = SHND(dst = os.getcwd() + "\\data\\shnd\\first",
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
            # continue
            break
