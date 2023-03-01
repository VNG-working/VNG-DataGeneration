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
        # self.img_name = "xuatkhau_{}.jpg".format(np.random.randint(665527))
        self.img_name = "fake_test.jpg"

        self.font_scale = np.random.randint(32, 35)
        self.original_font_scale = self.font_scale
        self.stamp_ink = (255, 51, 51)

        self.left_margin = randint(70, 80)
        self.line_height, self.original_line_height = [randint(65, 75)] * 2

        self.img_width = 1654
        self.img_height = 2339  # ratio w/h = ...

        self.bg_path = bg_path
        self.image = Image.open(self.bg_path).resize([self.img_width, self.img_height])

        self.draw = ImageDraw.Draw(self.image)

        self.cursor = [self.left_margin, 40]  # con trỏ đầu dòng
        self.line = 0

        # define cac loai font
        self.normal = ImageFont.truetype(
            "fonts/Courier/cour.ttf", size=self.font_scale-7)
        self.hsd = ImageFont.truetype(
            "fonts/Arial/ARIAL.ttf", size=self.font_scale-20)
        self.bold = ImageFont.truetype(
            "fonts/Tahoma/TAHOMA_0.ttf", size=self.font_scale-5)
        self.italic = ImageFont.truetype(
            "fonts/Arial/ARIALI.ttf", size=self.font_scale-10)
        self.big_bold = ImageFont.truetype(
            "fonts/Tahoma/TAHOMABD.ttf", size=self.font_scale)
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
        words = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        words_nums = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        base = (40, 45)
        scale = (25, 35, 45)
        newline = randint(30, 35)
        line = 35
        col_line = randint(5, 10)
        col_ft_line = randint(base[0], base[1])
        col_se_line = randint(base[0] + scale[0], base[1] + scale[0])
        col_rd_line = randint(base[0] + scale[1], base[1] + scale[1])
        col_fr_line = randint(base[0] + scale[2], base[1] + scale[2])

        # code
        self.col_cursor = randint(30, 40)   
        self.cursor[0] = self.col_cursor ++ randint(-10, 10)
        self.mark = self.cursor[0]
        self.cursor[1] += randint(5, 15)
        word_chose_lst = [randint(0, len(words)), randint(0, len(words)), randint(0, len(words))]
        raw_text = f"<{words[word_chose_lst[0]]}{words[word_chose_lst[1]]}{words[word_chose_lst[2]]}>"
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        # page
        self.col_cursor = randint(1500, 1550)
        self.cursor[0] = self.col_cursor ++ randint(-10, 10)
        self.mark = self.cursor[0]
        self.cursor[1] += randint(5, 15)
        
        raw_text = f"{randint(0, 10)} / {randint(0, 10)}"
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)
        
        # title
        self.col_cursor = randint(400, 450)
        self.cursor[0] = self.col_cursor ++ randint(-10, 10)
        self.mark = self.cursor[0]
        self.cursor[1] += randint(5, 15)
        
        raw_text = f"Tờ khai hàng hóa nhập khẩu (thông quan)"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.big_bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["doc_name"]*len(field_lst), self.big_bold)

        # so to khai
        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Số tờ khai"
        text = raw_text
        # field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["declaration_number_marker"], self.bold)

        self.cursor[0] = self.col_cursor ++ randint(220, 250)
        self.mark = self.cursor[0]
        raw_text = f"{randint(10**4, 10**5)}{randint(10**4, 10**5)}{randint(10**4, 10**5)}"
        text = raw_text
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["declaration_number"], self.normal)

        self.cursor[0] = self.col_cursor ++ randint(570, 590)
        self.mark = self.cursor[0]
        raw_text = f"Số tờ khai đầu tiên"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        # so to khai tam nhap
        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Số tờ khai tạm nhập tái xuất tương ứng"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        # ma phan loai kiem tra
        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Mã phân loại kiểm tra"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ randint(300, 310)
        self.mark = self.cursor[0]
        raw_text = f"{randint(0, 10)} {words[randint(0, len(words))]}"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        # ma loai hinh
        self.cursor[0] = self.col_cursor ++ randint(450, 460)
        self.mark = self.cursor[0]
        raw_text = f"Mã loại hình"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.cursor[0] = self.col_cursor ++ randint(650, 660)
        self.mark = self.cursor[0]
        raw_text = f"{words[randint(0, len(words))]}{randint(0, 100)}" + f"{randint(0, 10)} [{randint(0, 10)}]"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        self.cursor[0] = self.col_cursor ++ randint(900, 910)
        self.mark = self.cursor[0]
        raw_text = "Mã số hàng hóa điện của tờ khai"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.cursor[0] = self.col_cursor ++ randint(1430, 1450)
        self.mark = self.cursor[0]
        raw_text = f"{randint(1000, 10000)}"
        text = raw_text
        # field_lst = raw_text.split(" ")
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        # co quan hai quan
        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        len_cq = randint(8, 10)
        raw_text = f"Tên cơ quan Hải quan tiếp nhận tờ khai"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ randint(750, 760)
        self.mark = self.cursor[0]
        len_cq = randint(8, 10)
        raw_text = "".join([words[randint(0, len(words))] for x in range(len_cq)])
        text = raw_text
        
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.cursor[0] = self.col_cursor ++ randint(1000, 1020)
        self.mark = self.cursor[0]
        raw_text = "Mã bộ phận xử lí tờ khai"
        text = raw_text
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.cursor[0] = self.col_cursor ++ randint(1200, 1210)
        self.mark = self.cursor[0]
        raw_text = f"{randint(0, 99)}"
        text = raw_text

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        # ngay dang ki
        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Ngày đăng ký" 
        text = raw_text
        
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text] , ["text"], self.bold)

        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ randint(200, 210)
        self.mark = self.cursor[0]
        raw_text = f"{randint(0, 99)}/{randint(0, 99)}/{randint(10**3, 10**4)}" 
        text = raw_text
    
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text] , ["declaration_date"], self.normal)

        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ randint(380, 390)
        self.mark = self.cursor[0]
        raw_text = f"{randint(0, 99)}:{randint(0, 99)}:{randint(10**3, 10**4)}" 
        text = raw_text
    
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text] , ["text"], self.normal)

        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ randint(540, 550)
        self.mark = self.cursor[0]
        raw_text = f"Ngày thay đổi đăng kí"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ randint(800, 810)
        self.mark = self.cursor[0]
        raw_text = f"{randint(0, 99)}/{randint(0,99)}/{randint(10**3, 10**4)} {randint(0, 99)}:{randint(0,99)}:{randint(0, 99)}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ randint(1120, 1130)
        self.mark = self.cursor[0]
        raw_text = f"Thời hạn tái nhập/tái xuất"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        # line
        start_point = (20, self.cursor[1] + line)
        end_point = (1600, self.cursor[1] + line)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        # Nguoi nhap khau
        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Người nhập khẩu"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        # Ma so thue
        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Mã"
        text = raw_text

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ randint(120, 130)
        self.mark = self.cursor[0]
        raw_text = f"{randint(10**4, 10**5)}{randint(10**4, 10**5)}-{randint(10**3, 10**4)}"
        text = raw_text

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["importer_tax"], self.normal)

        # load cong ty 

        source_txt = os.getcwd() + "/ds_cty.txt"
        with open(source_txt, "r", encoding="utf-8") as f:
            lines = f.readlines()
            cty_lst = [x[:-1] for x in lines if "CÔNG TY" in x and "Mã số thuế" not in x]
            dc_lst = [x[:-1].split(":")[-1] for x in lines if "Địa chỉ" in x]
        
        # Cong ty
        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Tên"
        text = raw_text

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ randint(100, 120)
        self.mark = self.cursor[0]
        raw_text = f"{cty_lst[randint(0, len(cty_lst))]}"
        text = raw_text

        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["importer_name"]*len(field_lst), self.normal)

        # MST
        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Mã bưu chính"
        text = raw_text

        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ randint(220, 250)
        self.mark = self.cursor[0]
        raw_text = f"+({randint(0, 100)}){randint(0, 100)}"
        text = raw_text

        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        # DC
        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Địa chỉ"
        text = raw_text

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ randint(200, 220)
        self.mark = self.cursor[0]
        raw_text = dc_lst[randint(0, len(dc_lst))]
        text = raw_text

        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        # sdt
        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Số điện thoại"
        text = raw_text

        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ randint(200, 220)
        self.mark = self.cursor[0]
        raw_text = f"{randint(10**5, 10**6)}{randint(10**5, 10**6)}"
        text = raw_text

        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        # uy thac

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Người ủy thác nhập khẩu"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Mã"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Tên"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        # line
        start_point = (20, self.cursor[1] + line)
        end_point = (1600, self.cursor[1] + line)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        # nguoi xuat khau

        self.col_cursor = col_ft_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Người xuất khẩu"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_se_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Mã"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Tên"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ randint(100, 120)
        self.mark = self.cursor[0]
        raw_text = f"{cty_lst[randint(0, len(cty_lst))]}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Mã bưu chính"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ randint(300, 320)
        self.mark = self.cursor[0]
        raw_text = f"{randint(10, 100)}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Địa chỉ"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ randint(150, 170)
        self.mark = self.cursor[0]
        raw_text = dc_lst[randint(0, len(dc_lst))].upper().strip()
        text = raw_text
        print(raw_text)
        field_lst = raw_text.split(" ")
        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Mã nước"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_se_line
        self.cursor[0] = self.col_cursor ++ randint(180, 200)
        self.mark = self.cursor[0]
        raw_text = f"{words[randint(0, len(words))]}{words[randint(0, len(words))]}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Người ủy thác xuất khẩu"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        start_point = (20, self.cursor[1] + line)
        end_point = (1600, self.cursor[1] + line)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Đại lý hải quan"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = randint(900, 910)   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        # self.cursor[1] += randint(50, 60)
        raw_text = f"Mã nhân viên hải quan"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        start_point = (20, self.cursor[1] + line)
        end_point = (1600, self.cursor[1] + line)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        start_point = (800, self.cursor[1] + line)
        end_point = (800, self.cursor[1] + line*(newline - 10)/2)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Số vận đơn"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = randint(820, 840)   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]        
        raw_text = f"Địa điểm lưu kho"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = randint(820, 840)   
        self.cursor[0] = self.col_cursor ++ randint(300, 320)
        self.mark = self.cursor[0]        
        text_gen = "".join([words_nums[randint(0, len(words_nums))] for x in range(8)])
        raw_text = f"{text_gen}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.col_cursor = randint(1300, 1310)   
        self.cursor[0] = self.col_cursor ++ randint(50, 60)
        self.mark = self.cursor[0]        
        raw_text = f"CANG DICH VU"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        for x in range(5):
            self.col_cursor = col_se_line
            self.cursor[0] = self.col_cursor ++ col_line
            self.mark = self.cursor[0]
            self.cursor[1] += newline
            raw_text = f"{x}"
            text = raw_text
            field_lst = raw_text.split(" ")

            self.write(text, char_font=self.bold, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.bold)

            if x == 0:
                self.col_cursor = randint(820, 840)   
                self.cursor[0] = self.col_cursor ++ col_line
                self.mark = self.cursor[0]
                raw_text = "Địa điểm dỡ hàng"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.bold)

                self.col_cursor = randint(820, 840)   
                self.cursor[0] = self.col_cursor ++ randint(300, 320)
                self.mark = self.cursor[0]
                text_gen = "".join([words[randint(0, len(words))] for j in range(5)])
                raw_text = f"{text_gen}"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

                self.col_cursor = randint(1300, 1310)   
                self.cursor[0] = self.col_cursor ++ randint(50, 60)
                self.mark = self.cursor[0]        
                raw_text = f"CANG DICH VU - {words[randint(0, len(words))]}{words[randint(0, len(words))]}"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)
            
            elif x == 1:
                self.col_cursor = randint(820, 840)   
                self.cursor[0] = self.col_cursor ++ col_line
                self.mark = self.cursor[0]
                raw_text = "Địa điểm xếp hàng"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.bold)

                self.col_cursor = randint(820, 840)   
                self.cursor[0] = self.col_cursor ++ randint(300, 320)
                self.mark = self.cursor[0]
                text_gen = "".join([words[randint(0, len(words))] for j in range(5)])
                raw_text = f"{text_gen}"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

                self.col_cursor = randint(1300, 1310)   
                self.cursor[0] = self.col_cursor ++ randint(50, 60)
                self.mark = self.cursor[0]  
                text_gen = "".join([words[randint(0, len(words))] for j in range(5)])      
                raw_text = f"{text_gen}"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)
            
            elif x == 2:
                self.col_cursor = randint(820, 840)   
                self.cursor[0] = self.col_cursor ++ col_line
                self.mark = self.cursor[0]
                raw_text = "Phương tiện vận chuyển"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

            elif x == 3:
                self.col_cursor = randint(820, 840)   
                self.cursor[0] = self.col_cursor ++ randint(300, 320)
                self.mark = self.cursor[0]
                text_gen = "".join([str(randint(0, 10)) for j in range(4)])
                raw_text = f"{text_gen}"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

                self.col_cursor = randint(820, 840)   
                self.cursor[0] = self.col_cursor ++ randint(400, 420)
                self.mark = self.cursor[0]
                f1 = "".join([words[randint(0, len(words))] for x in range(5)])
                f2 = "".join([words[randint(0, len(words))] for x in range(6)])
                f3 = "".join([words_nums[randint(0, len(words_nums))] for x in range(5)])
                raw_text = f"{f1} {f2}/{f3}"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)
            
            elif x == 4:
                self.col_cursor = randint(820, 840)   
                self.cursor[0] = self.col_cursor ++ col_line
                self.mark = self.cursor[0]
                raw_text = "Ngày hàng đến"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

                self.col_cursor = randint(820, 840)   
                self.cursor[0] = self.col_cursor ++ randint(400, 430)
                self.mark = self.cursor[0]
                raw_text = f"{randint(0, 100)}/{randint(0, 100)}/{randint(10**2, 10**4)}"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.normal)

            if randint(0, 2) == 1:
                self.col_cursor = col_line   
                self.cursor[0] = self.col_cursor ++ randint(100, 120)
                self.mark = self.cursor[0]
                text_gen = "".join([words_nums[randint(0, len(words_nums))] for x in range(14)])
                raw_text = f"{text_gen}"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["waybill_number"], self.normal)
            
        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        text_gen = "Số lượng"
        raw_text = f"{text_gen}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)
        
        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(600, 630)
        self.mark = self.cursor[0]
        text_gen = f"{randint(0, 100)} {words[randint(0, len(words))]}{words[randint(0, len(words))]}"
        raw_text = f"{text_gen}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        self.col_cursor = randint(820, 840)   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        raw_text = "Ký hiệu và số hiệu"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        text_gen = "Tổng trọng lượng hàng (Gross)"
        raw_text = f"{text_gen}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(470, 520)
        self.mark = self.cursor[0]
        text_gen = f"{randint(0, 10)}.{randint(0, 1000)},{randint(0, 1000)} {words[randint(0, len(words))]}{words[randint(0, len(words))]}{words[randint(0, len(words))]}"
        raw_text = f"{text_gen}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        text_gen = "Số lượng container"
        raw_text = f"{text_gen}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(470, 520)
        self.mark = self.cursor[0]
        raw_text = f"{randint(0, 1000)}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.col_cursor = randint(820, 840)   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Ngày được phép nhận kho đầu tiên"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = randint(820, 840)   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Mã văn bản pháp quy khác"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        start_point = (20, self.cursor[1] + line)
        end_point = (1600, self.cursor[1] + line)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Số hóa đơn"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(200, 230)
        self.mark = self.cursor[0]
        f5 = "".join([words_nums[randint(0, len(words_nums))] for x in range(14)])
        raw_text = f"{words[randint(0, len(words))]} * {f5}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["invoice_number"], self.normal)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Số tiếp nhận hóa đơn điện tử"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Ngày phát hành"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(470, 520)
        self.mark = self.cursor[0]
        raw_text = f"{randint(0, 100)}/{randint(0, 100)}/{randint(10**2, 10**3)}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Phương thức thanh toán"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(400, 430)
        self.mark = self.cursor[0]
        raw_text = f"{words[randint(0, len(words))]}{words[randint(0, len(words))]}{words[randint(0, len(words))]}"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Tổng giá trị hóa đơn"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(400, 430)
        self.mark = self.cursor[0]
        raw_text = f"{words[randint(0, len(words))]} - {words[randint(0, len(words))]}{words[randint(0, len(words))]}{words[randint(0, len(words))]} - {words[randint(0, len(words))]}{words[randint(0, len(words))]}{words[randint(0, len(words))]} - "
        text = raw_text
        # field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["currency"], self.normal)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(670, 730)
        self.mark = self.cursor[0]
        raw_text = "{:,}".format(randint(10**5, 10**8))
        text = raw_text
        # field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["total_amount"], self.normal)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Tổng giá trị tính thuế"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(670, 730)
        self.mark = self.cursor[0]
        raw_text = "{:,}".format(randint(10**5, 10**8))
        text = raw_text
        # field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Tổng hệ số phân bố trị giá"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_line   
        self.cursor[0] = self.col_cursor ++ randint(670, 730)
        self.mark = self.cursor[0]
        raw_text = "{:,}".format(randint(10**5, 10**8))
        text = raw_text

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Mã kết quả kiểm tra nội dung"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        start_point = (20, self.cursor[1] + line)
        end_point = (1600, self.cursor[1] + line)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Giấy phép nhập khẩu"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.cursor[1] += newline - 10
        for idx, x in enumerate([col_line, randint(700, 710), randint(1400, 1410)]):
            self.col_cursor = col_se_line   
            self.cursor[0] = self.col_cursor ++ x
            self.mark = self.cursor[0]
            raw_text = f"{idx+1}"
            text = raw_text

            self.write(text, char_font=self.bold, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.bold)

            self.col_cursor = col_se_line   
            self.cursor[0] = x ++ randint(150, 170)
            self.mark = self.cursor[0]
            raw_text = f"-"
            text = raw_text

            self.write(text, char_font=self.bold, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        self.cursor[1] += newline - 10
        for idx, x in enumerate([col_line, randint(700, 710), randint(1400, 1410)]):
            self.col_cursor = col_se_line   
            self.cursor[0] = self.col_cursor ++ x
            self.mark = self.cursor[0]
            raw_text = f"{idx+4}"
            text = raw_text

            self.write(text, char_font=self.bold, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.bold)

            self.col_cursor = col_se_line   
            self.cursor[0] = x ++ randint(150, 170)
            self.mark = self.cursor[0]
            raw_text = f"-"
            text = raw_text

            self.write(text, char_font=self.bold, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        start_point = (20, self.cursor[1] + line)
        end_point = (1600, self.cursor[1] + line)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Mã phân loại trị giá"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ randint(400, 410)
        self.mark = self.cursor[0]
        raw_text = f"{randint(0, 10)}"
        text = raw_text

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        self.col_cursor = col_se_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Khai trị giá tổng hợp"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        for x in [randint(350, 360), randint(500, 510), randint(1200, 1210)]:
            self.col_cursor = col_ft_line   
            self.cursor[0] = self.col_cursor ++ x
            self.mark = self.cursor[0]
            raw_text = f"-"
            text = raw_text

            self.write(text, char_font=self.normal, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.normal)
        
        self.col_cursor = col_se_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Các khoản điều chỉnh"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_rd_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Phí vận chuyển"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        for x in [randint(350, 360), randint(500, 510)]:
            self.col_cursor = col_ft_line   
            self.cursor[0] = self.col_cursor ++ x
            self.mark = self.cursor[0]
            raw_text = f"-"
            text = raw_text

            self.write(text, char_font=self.normal, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.normal)
        
        self.col_cursor = col_rd_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Phí bảo hiểm"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        for x in [randint(350, 360), randint(500, 510)]:
            self.col_cursor = col_ft_line   
            self.cursor[0] = self.col_cursor ++ x
            self.mark = self.cursor[0]
            raw_text = f"-"
            text = raw_text

            self.write(text, char_font=self.normal, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.normal)
        
        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Mã tên"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(250, 260)
        self.mark = self.cursor[0]
        raw_text = "Mã phân loại"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(550, 560)
        self.mark = self.cursor[0]
        raw_text = "Trị giá khoản điều chỉnh"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(1100, 1110)
        self.mark = self.cursor[0]
        raw_text = "Tổng hệ số phân bố"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        for idx in range(5):
            self.col_cursor = col_rd_line   
            self.cursor[0] = self.col_cursor ++ col_line
            self.mark = self.cursor[0]
            self.cursor[1] += newline
            raw_text = f"{idx+1}"
            text = raw_text

            self.write(text, char_font=self.bold, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.bold)

            for x in [randint(350, 360), randint(500, 510), randint(700, 710)]: 
                self.cursor[0] = self.col_cursor ++ x
                self.mark = self.cursor[0]
                raw_text = f"-"
                text = raw_text

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.normal)

        start_point = (20, self.cursor[1] + line)
        end_point = (1600, self.cursor[1] + line)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        self.col_cursor = col_ft_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Chi tiết khai trị giá"
        text = raw_text

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ col_line
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = "Tên sắc thuế"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(250, 260)
        self.mark = self.cursor[0]
        raw_text = "Tổng tiền thuế"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(550, 560)
        self.mark = self.cursor[0]
        raw_text = "Số dòng tổng"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        for idx in range(6):
            self.cursor[1] += newline

            self.col_cursor = col_rd_line   
            self.cursor[0] = self.col_cursor ++ col_line
            self.mark = self.cursor[0]
            raw_text = f"{idx + 1}"
            text = raw_text

            self.write(text, char_font=self.bold, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.bold)

            if randint(0, 2) == 1:
                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(50, 60)
                self.mark = self.cursor[0]
                raw_text = f"{words[randint(0, len(words))]}"
                text = raw_text

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.normal)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(110, 120)
                self.mark = self.cursor[0]
                lencq = randint(2, 5)
                sub = "".join([words[randint(0, len(words))] for x in range(lencq)])
                raw_text = f"Thuế {sub}"
                text = raw_text

                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(300, 310)
                self.mark = self.cursor[0]
                raw_text = f"{randint(10**6, 10**7)}"
                text = raw_text

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.normal)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(600, 610)
                self.mark = self.cursor[0]
                raw_text = f"{randint(0, 10)}"
                text = raw_text

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.normal)
            
            self.col_cursor = col_fr_line   
            self.cursor[0] = self.col_cursor ++ randint(450, 460)
            self.mark = self.cursor[0]
            raw_text = f"VND"
            text = raw_text

            self.write(text, char_font=self.bold, ink=randink(True))
            self.get_marker_coord(text, [raw_text], ["text"], self.bold)

            if idx == 0:
                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(700, 710)
                self.mark = self.cursor[0]
                raw_text = f"Tổng tiền thuế phải nộp"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(1050, 1060)
                self.mark = self.cursor[0]
                raw_text = f"{randint(10**6, 10**7)}"
                text = raw_text

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.normal)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(1200, 1210)
                self.mark = self.cursor[0]
                raw_text = f"VND"
                text = raw_text

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.bold)
            
            if idx == 1:
                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(700, 710)
                self.mark = self.cursor[0]
                raw_text = f"Số tiền bảo lãnh"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(1200, 1210)
                self.mark = self.cursor[0]
                raw_text = f"VND"
                text = raw_text

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.bold)
            
            if idx == 2:
                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(700, 710)
                self.mark = self.cursor[0]
                raw_text = f"Tỷ giá tính thuế"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(1000, 1010)
                self.mark = self.cursor[0]
                raw_text = f"USD"
                text = raw_text

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.bold)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(1200, 1210)
                self.mark = self.cursor[0]
                raw_text = f"{randint(10**6, 10**7)}"
                text = raw_text

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.normal)
            
            if idx == 5:
                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(700, 710)
                self.mark = self.cursor[0]
                raw_text = f"Mã xác định thời hạn nộp thuế"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(1100, 1110)
                self.mark = self.cursor[0]
                raw_text = f"{words[randint(0, len(words))]}"
                text = raw_text

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.bold)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(1150, 1160)
                self.mark = self.cursor[0]
                raw_text = f"Người nộp thuế"
                text = raw_text
                field_lst = raw_text.split(" ")

                self.write(text, char_font=self.normal, ink=randink(True))
                self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

                self.col_cursor = col_fr_line   
                self.cursor[0] = self.col_cursor ++ randint(1400, 1410)
                self.mark = self.cursor[0]
                raw_text = f"{randint(0, 10)}"
                text = raw_text
                # field_lst = raw_text.split(" ")

                self.write(text, char_font=self.bold, ink=randink(True))
                self.get_marker_coord(text, [raw_text], ["text"], self.bold)
            
        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(700, 710)
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Mã lí do đề nghị BP"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(1150, 1160)
        self.mark = self.cursor[0]
        raw_text = f"Phân loại nộp thuế"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.normal, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.normal)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(1500, 1510)
        self.mark = self.cursor[0]
        raw_text = f"{words[randint(0, len(words))]}"
        text = raw_text
        # field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        start_point = (20, self.cursor[1] + line)
        end_point = (1600, self.cursor[1] + line)
        self.draw.line([start_point, end_point], fill = (0, 0, 0), width = 3)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(600, 610)
        self.mark = self.cursor[0]
        self.cursor[1] += newline
        raw_text = f"Tổng số trang của tờ khai"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(1000, 1010)
        self.mark = self.cursor[0]
        raw_text = f"{words[randint(0, len(words))]}"
        text = raw_text
        # field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(1100, 1110)
        self.mark = self.cursor[0]
        raw_text = f"Tổng số dòng hàng của tờ khai"
        text = raw_text
        field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, field_lst, ["text"]*len(field_lst), self.bold)

        self.col_cursor = col_fr_line   
        self.cursor[0] = self.col_cursor ++ randint(1500, 1510)
        self.mark = self.cursor[0]
        raw_text = f"{randint(0, 10)}"
        text = raw_text
        # field_lst = raw_text.split(" ")

        self.write(text, char_font=self.bold, ink=randink(True))
        self.get_marker_coord(text, [raw_text], ["text"], self.bold)


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
        self.fake_stamp(xmin = 1000, xmax = 1400, ymin = 100, ymax = 300)
        self.fake_stamp(xmin = 1000, xmax = 1400, ymin = 400, ymax = 600)
        self.fake_stamp(xmin = 1250, xmax = 1400, ymin = 50, ymax = 200, blue = True)
        self.fake_stamp(xmin = 1100, xmax = 1250, ymin = 700, ymax = 850, blue = True)
        self.fake_stamp(xmin = 1500, xmax = 1650, ymin = 800, ymax = 950, blue = True)
        # if np.random.rand() < 0.8:
        #     self.vien_trang()
        # if np.random.rand() < 0.3:
        #     self.ep_plastic()
            
        self.fake_general_image(add_crease = False, add_fold = False)

        self.save()


if __name__ == '__main__':
    i = 0
    while i < 1:
        print("_______________________________________________________________________________________________________________")
        try:
            faker = SHND(dst = os.getcwd() + "\\data_xuatkhau\\",
                bg_path = os.getcwd() + "\\bg\\xuatkhau\\bg.png",
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

        # faker = SHND(dst = os.getcwd() + "\\data_xuatkhau\\",
        #     bg_path = os.getcwd() + "\\bg\\xuatkhau\\bg.png",
        #     font_dir = os.getcwd() + "\\fonts\\Times New Roman")
        # print(faker.characters)
        # faker.fake()
        # print(faker.img_name)
        # print("faking")
        # i += 1