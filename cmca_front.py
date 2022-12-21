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
labels_list = []


class CMCA(OfficialID):
    def __init__(self, dst='data/cmca/front/'):
        super().__init__(dst)
        # dst = 'data/test/'
        self.dst = dst
        self.img_name = "cmca_front_fake_{}.jpg".format(np.random.randint(665527))
        # self.img_name = "fake_test.jpg"

        self.font_scale = np.random.randint(48, 55)
        self.original_font_scale = self.font_scale
        self.stamp_ink = (255, 51, 51)

        self.left_margin = randint(45, 55)
        self.line_height, self.original_line_height = [randint(65, 75)] * 2

        self.img_width = 1980
        self.img_height = 1200  # ratio w/h = 1.6

        bg_path = np.random.choice(glob.glob("bg/cmca/front/*"))
        self.image = Image.open(bg_path).resize([self.img_width, self.img_height])

        self.draw = ImageDraw.Draw(self.image)

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
        # chxhcvn
        self.cursor[0] = randint(750, 950)
        self.cursor[1] = randint(50, 70)
        raw_text = 'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM'
        text = raw_text
        font = ImageFont.truetype('fonts/AvrileSerif-SemiBold.ttf', randint(40, 45))
        self.write(text, font, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ['outlier'], font)

        # line
        length = 700 + randint(-50, 50)
        center_x = self.cursor[0] + self.get_text_length(text, font) // 2
        self.cursor[0] = center_x - length // 2
        pt1 = (self.cursor[0], self.cursor[1] +self.line_height-10)
        pt2 = (self.cursor[0] + length, self.cursor[1] +self.line_height-10)
        self.draw.line([pt1, pt2], fill=randink(), width=randint(1, 5))

        # giay cmcand
        self.cursor[0] = randint(700, 950)
        self.cursor[1] += randint(50, 100)
        raw_text = "GIẤY CHỨNG MINH CÔNG AN NHÂN DÂN"
        text = raw_text
        font = ImageFont.truetype('fonts/HeadingNowTrial-56Bold.ttf', self.font_scale+randint(15, 25))
        self.write(text, char_font=font, ink=(182, 31, 34))
        self.get_field_coord(text, [raw_text], ["outlier"], font)
        
        # so
        self.cursor[0] = randint(1030, 1200)
        self.cursor[1] = self.cursor[1] + randint(70, 110)
        raw_text = "Số:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, [raw_text], ["marker_number"], self.normal)
        
        # autual so
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(30, 70)
        raw_text = random_number(3) + '  -  ' + random_number(3)
        text = raw_text
        self.write(text, char_font=self.big_bold, ink=randink(True))
        self.get_field_coord(text, [raw_text], ["number"], self.big_bold)


        # ho ten
        self.col_cursor = randint(650, 720)
        if self.col_cursor < self.br_poitrait[0]:
            self.col_cursor = self.br_poitrait[0]+randint(50, 150)
        self.cursor[0] = self.col_cursor ++ randint(-30, 30)
        self.cursor[1] += randint(80, 120)
        raw_text = "Họ tên:"
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["marker_name"], self.normal)

        # actual ho ten
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(140, 300)
        name = np.random.choice(self.names).upper()
        raw_text = name
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ["name"], self.bold)

        # ngay sinh
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] += self.line_height + randint(-10, 10)
        raw_text = "Ngày sinh:"
        text = raw_text
        self.write(text, char_font=self.normal, bold=True)
        self.get_marker_coord(text, [raw_text], ["marker_dob"], self.normal)

        # actual ngay sinh
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(140, 300)
        raw_text = random_date()
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ["dob"], self.bold)

        # cap bac
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] += self.line_height + randint(-10, 10)
        raw_text = "Cấp bậc:"
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["marker_rank"], self.normal)

        # actual cap bac
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(150, 300)
        capbac = np.random.choice([
            "Cấp tá",
            "Cấp tướng",
            "Hạ sĩ quan",
            'Cấp uý',
            'Cấp thượng tá',
            'Cấp thượng tướng',
            'Cấp thượng uý',
            'Cấp thượng hạ sĩ quan',
            'Cấp bách',
            'Cấp tính',
            'Cấp sĩ',
            'Cấp hạ sĩ',
        ])
        raw_text = capbac
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_field_coord(text, [raw_text], ["rank"], self.bold)

        # chuc vu
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] += self.line_height + randint(-10, 10)
        raw_text = "Chức vụ:"
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["marker_position"], self.normal)

        # actual chuc vu
        chucvu = np.random.choice([
            "Sĩ quan nghiệp vụ",
            "Hạ sĩ quan nghiệp vụ",
            "Đội trưởng",
            'Điều tra viên cao cấp',
            "Đội phó",
            "Sĩ quan CMKT"
            'Điều tra viên',
            'Phó đội trưởng',
            'Phó đội phó',
            'Điều tra viên trung cấp',
            'Điều tra viên hạ cấp',
            'Điều tra viên thường',
            'Hạ sĩ quan',
            'Phó CA huyện',
            'Phó CA tỉnh',
            'Phó CA thành phố',
            'Phó CA quận',
            'Phó CA phường',
            'Phó CA xã',
            'Trưởng CA huyện',
            'Trưởng CA tỉnh',
            'Trưởng CA thành phố',
            'Chuyên viên',
            'Điều phối viên',
            'Giám sát',
            'Giám đốc CA thành phố',
            'Giám đốc CA tỉnh',
        ])

        self.cursor[0] += self.get_text_length(text, self.normal) + randint(140, 190)
        raw_text = chucvu
        text = raw_text
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_field_coord(text, [raw_text], ["position"], self.bold)

        # don vi
        self.cursor[0] = self.col_cursor + randint(-30, 30)
        self.cursor[1] += self.line_height + randint(-10, 10)
        raw_text = "Đơn vị:"
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["marker_pow"], self.normal)
        

        # actual don vi
        self.cursor[0] += self.get_text_length(text, self.normal) + randint(30, 200)
        if self.district_type == "Huyện":
            dt = "H"
        elif self.district_type == "Quận":
            dt = "Q"
        elif "ã" in self.district_type:
            dt = "TX"
        else:
            dt = self.district_type
        if self.province_type == "Thành Phố":
            pt = "TP"
        else:
            pt = self.province_type
        r = randint(1,100)
        c = np.random.choice(list(string.ascii_uppercase))
        d = np.random.choice(list(string.ascii_uppercase))        
        donvi = np.random.choice([
            f"CA{dt}.{self.district}-{pt} {self.province}",
            f"CA{dt}.{self.district}-{self.province}",
            f"CA{dt}.{self.district}-{pt} {self.province}",
            f"CA{dt}.{self.district}-{self.province}",
            f"CA{dt}.{self.district}-{pt} {self.province}",
            f"CA{dt}.{self.district}-{self.province}",
            f"CA {pt} {self.province}",
            f"CA {pt} {self.province}",
            f"CA {pt} {self.province}",
            f"PC{r} - Phòng CS TP TTXH",
            f"Phòng Cảnh sát PC&CC {dt}.{self.district}",
            f"Phòng Cảnh sát PC&CC {pt}.{self.province}",
            f"{c}{r} - Bộ Công An",
            f"{c}{d}{r}-Công an {pt} {self.province}"
            
        ])
        raw_text = donvi
        text = raw_text
        self.write(text, char_font=self.roboto, ink=randink(True))
        self.get_field_coord(text, [raw_text], ["pow"], self.roboto)


        # ngay thang 
        date = str(np.random.randint(1, 32))
        month = str(np.random.randint(1, 13))
        year = str(np.random.randint(1000, 3000))

        date = '0' + date if len(date)==1 and np.random.rand() < 0.5 else date
        month = '0' + month if len(month)==1 and np.random.rand() < 0.5 else month

        raw_text = f'Ngày {date} tháng {month} năm {year}'
        text = raw_text
        self.cursor[0] = randint(1050, 1350)
        self.cursor[1] += self.line_height + randint(-10, 10)
        self.write(text, char_font=self.italic, bold=True)
        self.get_field_coord(text, [date, month, year], ["doi", 'doi', 'doi'], self.italic)
        
        # chuc vu nguoi ki
        center_x = self.cursor[0] + self.get_text_length(text, self.italic) // 2
        chucvuki = np.random.choice([
            f"GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            f"PHÓ GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            f"GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            f"PHÓ GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            f"GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            f"PHÓ GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            f"GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            f"PHÓ GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            f"GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            f"PHÓ GIÁM ĐÔC CÔNG AN {pt.upper()} {self.province.upper()}",
            "BỘ TRƯỞNG"
        ])
        raw_text = chucvuki
        text = raw_text
        font = ImageFont.truetype("fonts/cccd_text_bold.ttf", size=self.font_scale-10)
        self.cursor[0] = center_x - self.get_text_length(text, font) // 2 + randint(-80, 80)
        self.cursor[1] += self.line_height + randint(-10, 10)
        self.write(text, char_font=font, ink=randink(bold=True))
        self.get_field_coord(text, [raw_text], ["signer_position"], font)

        # ten nguoi ky
        center_x = self.cursor[0] + self.get_text_length(text, font) // 2
        name = np.random.choice(self.names)
        capbac = np.random.choice([
            'Đại tá',
            'Thiếu tướng',
            'Trung tướng',
            'Thượng tướng',
            'Đại tướng',
            "Chuẩn Đô Đốc",
            "Đô Đốc",
            "Thượng Đô Đốc",
        ])
        self.cursor[0] = randint(900, 1200)
        self.cursor[1] += self.line_height + randint(-10, 10)
        raw_text = capbac+ ' ' + name
        text = raw_text
        self.cursor[0] = center_x - self.get_text_length(text, self.bold) // 2 + randint(-80, 80)
        self.cursor[1] = randint(1000, 1100)
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_field_coord(text, [capbac, name], ["signer_rank", "signer_name"], self.bold)


        # nhom mau
        self.cursor[0] = randint(150, 250)
        self.cursor[1] = self.br_poitrait[1] + randint(0, 80)
        raw_text = "Nhóm máu:"
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["marker_blood"], self.normal)

        # actual nhom mau
        self.cursor[0] += self.get_text_length(text, self.bold) + randint(0, 70)
        self.cursor[1] += randint(-20, 20)
        nhommau = np.random.choice([
            "A","B","O","AB",
        ] + list(string.ascii_uppercase)) + np.random.choice(["+", "-", ''])
        raw_text = nhommau
        text = raw_text
        self.Bold_BLOOD = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale-5)
        self.write(text, char_font=self.Bold_BLOOD, ink=randink(True))
        self.get_field_coord(text, [raw_text], ["blood"], self.Bold_BLOOD)

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
        self.fake_stamp()
        self.fake_potrait()
        self.fakeMainInfo()
        if np.random.rand() < 0.4:
            self.fake_BG()
        self.fake_glare()
        self.fake_blur()
        self.fake_logo()
        self.fake_sign()

        if np.random.rand() < 0.8:
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
            faker = CMCA()
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
