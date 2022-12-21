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

    
class CMSQ_FRONT(OfficialID):
    def __init__(self, dst='data/cmsq/front/'):
        super().__init__(dst)
        # dst = 'data/test/'
        self.dst = dst
        self.img_name = "cmsq_front_fake_{}.jpg".format(np.random.randint(665527))
        # self.img_name = "fake_test.jpg"

        self.font_scale = np.random.randint(53, 54)
        self.original_font_scale = self.font_scale
        self.stamp_ink = (255, 51, 51)

        self.left_margin = randint(45, 55)
        self.line_height, self.original_line_height = [randint(80, 81)] * 2

        self.img_width = 1980
        self.img_height = 1200 # ratio w/h = 1.6

        bg_path = np.random.choice(glob.glob("bg/cmsq/front/*"))
        self.image = Image.open(bg_path).resize([self.img_width, self.img_height])

        self.draw = ImageDraw.Draw(self.image)

        self.cursor = [self.left_margin, 40]  # con trỏ đầu dòng
        self.line = 0

        # define cac loai font
        self.normal = ImageFont.truetype(
            "fonts/Arial/ARIAL.ttf", size=self.font_scale)
        # self.Bold = ImageFont.truetype(
        #     "fonts/texgyreheros-bold.otf", size=self.font_scale)
        self.Bold = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale)
        self.italic = ImageFont.truetype(
            "fonts/Arial/ARIALI.ttf", size=self.font_scale-7)
        self.Big_Bold = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale + 10)
        self.Small_Bold = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale - randint(7, 13))
        self.Bold_Italic = ImageFont.truetype(
            "fonts/Arial/ARIALBI.ttf", size=self.font_scale)
    
        self.hsd = ImageFont.truetype(
            "fonts/texgyreheros-bold.otf", size=self.font_scale-randint(12, 20))

        self.chxh = ImageFont.truetype('fonts/Bogart-Bold-trial.ttf', size=self.font_scale-10)

        if np.random.rand() < 0.5:
            self.semi_bold = ImageFont.truetype('fonts/Roboto-Medium.ttf', self.font_scale)
        else:
            self.semi_bold = ImageFont.truetype('fonts/Arial/ARIAL.ttf', self.font_scale)


        self.bbs = {
            "version": "5.0.1",
            "flags": {},
            "shapes": [],
            "imagePath": self.img_name,
            "imageHeight": self.img_height,
            "imageWidth": self.img_width
        }


        self.info = pd.read_csv("personal_info/eID_1000_front_v2.0.11 - eID_1000_front_v2.0.11.csv")
        n = len(self.info)
        self.province = eval(self.info.loc[np.random.randint(n)][9])["province"]
        self.province_type = eval(self.info.loc[np.random.randint(n)][9])["province_type"]
        self.poi = self.province_type + " " + self.province
        self.president = self.info.loc[np.random.randint(n)][2]
        self.names, self.addresses = get_info()
        self.characters = list(string.ascii_uppercase + string.digits)
        

        self.blocks = []
        self.fields = []

        # block related
        self.xmax = 0
        self.ymax = 0
        self.xmin = 2500

        # self.ink = tuple([int(np.random.normal(80, 20))] * 4)


    def fake_BG(self):
        bg_path = np.random.choice(glob.glob("bg/cmsq/front/*"))
        bg = Image.open(bg_path)
        # start = time.time()
        i = np.random.randint(4)
        bg = bg.resize([self.img_width, self.img_height])

        bg = np.array(bg)  # .getdata()).reshape(bg.size[1], bg.size[0], 3)
        image = np.array(self.image.convert('RGB'))
        bg = bg * 1./255
        image = (bg * image).astype(np.uint8)

        self.image = Image.fromarray(image)


    def fakeMainInfo(self):
        # chxhcnvn
        self.cursor = [470+randint(-20, 20), 10]
        text = 'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM'
        
        r, g, b = self.stamp_sign_ink
        text = self.write(text, self.chxh, ink=(r+randint(-30, 30), g+randint(-30, 30), b+randint(-30, 30)))
        self.get_field_coord(text, [text], ['outlier'], self.chxh)

        # giay cmsq
        self.cursor[0] = 750 + randint(-50, 50)
        self.cursor[1] = 141 + randint(-10, 10)
        text = "GIẤY CHỨNG MINH SĨ QUAN"
        
        self.Bold_huge = ImageFont.truetype(
            "fonts/Arial/ARIALBD.ttf", size=self.font_scale+randint(10, 20))
        text = self.write(text, char_font=self.Bold_huge, ink=(187+randint(-20, 20),43+randint(-20, 20),33+randint(-20, 20)))
        self.get_field_coord(text, [text], ["outlier"], self.Bold_huge)
        
        # so
        self.cursor[0] = 1100 + randint(-100, 100)
        self.cursor[1] += self.line_height + randint(5, 30)
        text = "Số:"
        
        text = self.write(text, char_font=self.Bold, ink=randink(True))
        self.get_marker_coord(text, [text], ["marker_number"], self.Bold)

        # actual so
        self.cursor[0] += self.get_text_length(text, self.Bold) + randint(5, 80)
        self.cursor[1] += randint(-10, 10)
        p1 = str(randint(10,100))
        p2 = str(randint(100,1000))
        p3 = str(randint(100,1000))
        num = p1+ " " + p2+ " " + p3
        text = num
        
        text = self.write(text, char_font=self.Bold, ink=randink(True))
        self.get_marker_coord(text, [text], ["number"], self.Bold)
        
        
        # ho ten
        self.col_cursor = 640
        if self.col_cursor < self.br_poitrait[0]:
            self.col_cursor = self.br_poitrait[0] + randint(50, 100)
        self.cursor[0] = self.col_cursor + randint(-50, 50)
        self.cursor[1] += self.line_height + randint(40, 50)
        text = "Họ tên:"
        
        text = self.write(text, char_font=self.Bold, ink=randink(True))
        self.get_marker_coord(text, [text], ["marker_name"], self.Bold)
        
        # actual ho ten
        self.cursor[0] += self.get_text_length(text, self.Bold) + randint(30, 300)
        self.cursor[1] += randint(-10, 10)
        name = np.random.choice(self.names).upper() 
        text = name
        
        text = self.write(text, char_font=self.Bold, ink=randink(extra_bold=True))
        self.get_field_coord(text, [text], ["name"], self.Bold)
        

        # cap bac
        self.cursor[0] = self.col_cursor + randint(-50, 50)
        self.cursor[1] += self.line_height + randint(-10, 10)
        text = "Cấp bậc:"
        
        text = self.write(text, char_font=self.Bold, ink=randink(True))
        self.get_marker_coord(text, [text], ["marker_ranking"], self.Bold)

        # actual cap bac
        self.cursor[0] += self.get_text_length(text, self.Bold) + randint(50, 300)
        self.cursor[1] += randint(-10, 10)
        capbac = np.random.choice([
            'Thiếu tướng',
            'Trung tướng',
            'Đại tướng',
            'Thượng Tướng',
            'Đại tá',
            'Thượng tá',
            'Trung tá',
            'Thiếu tá',
            'Cấp uý',
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
            'Thiếu úy',
            'Đại úy',
            'Trung úy',
            'Thiếu úy',
            'Hạ sĩ',
            'Thượng sĩ'
        ])
        text = capbac
        
        text = self.write(text, char_font=self.semi_bold, ink = randink())
        self.get_field_coord(text, [text], ["ranking"], self.semi_bold)

        
        # don vi cap
        self.cursor[0] = self.col_cursor + randint(-50, 50)
        self.cursor[1] += self.line_height + randint(-10, 10)
        text = "Đơn vị cấp:"
        
        text = self.write(text, char_font=self.Bold, ink=randink(True))
        self.get_marker_coord(
            text, [text], ["marker_pow"], self.Bold)

        # actual don vi cap
        self.cursor[0] += self.get_text_length(text, self.Bold) + randint(50, 200)
        self.cursor[1] += randint(-10, 10)
        donvi = np.random.choice([
            'Bộ Tổng Tham mưu',
            'Tổng cục Chính trị',
            'Tổng cục 2',
            'Tổng cục Hậu cần',
            'Tổng cục Kỹ thuật',
            'Tổng cục Công nghiệp Quốc phòng',
            'Quân chủng Hải quân',
            'Quân chủng Phòng không - Không quân',
            'BTL Bộ đội Biên phòng',
            'BTL Cảnh sát biển',
            'BTL Tác chiến không gian mạng',
            'BTL Bảo vệ Lăng Chủ tịch Hồ Chí Minh',
            'BTL Thủ đô Hà Nội',
            f'Quân khu {randint(1, 100)}',
            f'Quân đoàn {randint(1, 100)}',
            f'Quân chủng {np.random.choice(["Lục quân", "Hải quân", "Không quân", "Phòng không", "Biên phòng"])}',
            f'{np.random.choice(["Binh chủng", ""], p=[0.8, 0.2])} {np.random.choice(["Binh chủng", "Bộ binh", "Tăng-Thiết giáp", "Pháo binh", "Công binh", "Đặc công", "Nhảy dù", "Xạ thủ bắn tỉa", "Tên lửa phòng không", "Pháo phòng không", "Radar phòng không", "Không quân tiêm kích", "Không quân oanh tạc", "Không quân cường kích", "Nhảy dù", "Hải quân hạm nổi", "Hải quân tàu ngầm", "Không lực hải quân", "Đặc công nước", "Thủy quân lục chiến", "Radar phòng hải", "Tác chiến điện tử", "Tên lửa chiến lược", "Hoá học", "Kỵ binh", "Trinh sát", "Thông tin-viễn thông quân sự", "Vận tải quân sự", "Kỹ thuật quân sự", "Quân y", "Hậu cần quân sự"])}'
        ])
        text = donvi
        
        text = self.write(text, char_font=self.semi_bold, ink = randink())
        self.get_field_coord(text, [text], ["pow"], self.semi_bold)
        

        # ngay thang
        self.cursor[0] = randint(900, 1200)
        self.cursor[1] += self.line_height + randint(-10, 10)
        date = str(np.random.randint(1, 32))
        month = str(np.random.randint(1, 13))
        year = str(np.random.randint(1000, 3000))

        date = '0' + date if len(date)==1 and np.random.rand() < 0.5 else date
        month = '0' + month if len(month)==1 and np.random.rand() < 0.5 else month

        text = f'Ngày {date} tháng {month} năm {year}'
        
        if np.random.rand() < 0.5:
            ink = randink(bold=True)
        else:
            ink = randink()
        text = self.write(text, self.italic, ink=ink)
        self.get_field_coord(text, [date, month, year], ['doi']*3, self.italic)
      
        
        # chuc vu nguoi ki
        center_x = self.cursor[0] + self.get_text_length(text, self.italic)//2
        ten_quan_khu = randint(1,10)
        chucvuki= np.random.choice([
            'CHÍNH ỦY',
            f"CHÍNH ỦY QUÂN KHU {ten_quan_khu}",
            "CHÍNH ỦY QUÂN CHỦNG HẢI QUÂN",
            "CHÍNH ỦY QUÂN CHỦNG KHÔNG QUÂN",
            "CHÍNH ỦY QUÂN CHỦNG BIÊN PHÒNG",
            "CHÍNH ỦY QUÂN CHỦNG LỤC QUÂN",
            "CHÍNH ỦY QUÂN CHỦNG PHÁO BINH",
            "CHÍNH ỦY QUÂN CHỦNG CÔNG BINH",
            "CHÍNH ỦY QUÂN CHỦNG ĐẶC CÔNG",
            f'Quân chủng {np.random.choice(["Lục quân", "Hải quân", "Không quân", "Phòng không", "Biên phòng"])}',
            f'{np.random.choice(["Binh chủng", ""], p=[0.8, 0.2])} {np.random.choice(["Binh chủng", "Bộ binh", "Tăng-Thiết giáp", "Pháo binh", "Công binh", "Đặc công", "Nhảy dù", "Xạ thủ bắn tỉa", "Tên lửa phòng không", "Pháo phòng không", "Radar phòng không", "Không quân tiêm kích", "Không quân oanh tạc", "Không quân cường kích", "Nhảy dù", "Hải quân hạm nổi", "Hải quân tàu ngầm", "Không lực hải quân", "Đặc công nước", "Thủy quân lục chiến", "Radar phòng hải", "Tác chiến điện tử", "Tên lửa chiến lược", "Hoá học", "Kỵ binh", "Trinh sát", "Thông tin-viễn thông quân sự", "Vận tải quân sự", "Kỹ thuật quân sự", "Quân y", "Hậu cần quân sự"])}',
            "CHÍNH ỦY QUÂN CHỦNG PK-KQ",
            "PHÓ CHỦ NHIỆM TCCT",
            f"TƯ LỆNH QUÂN KHU {ten_quan_khu}",
            f"PHÓ TƯ LỆNH QUÂN KHU {ten_quan_khu}",
            f'TỔNG GIÁM ĐỐC QUÂN KHU {ten_quan_khu}',
            f'TỔNG CỤC TRƯỞNG TỔNG CỤC {randint(1, 20)}'
        ]).upper()
        text = chucvuki
        
        self.cursor[0] = center_x - self.get_text_length(text, self.Small_Bold) // 2 + randint(-30, 30)
        self.cursor[1] += self.line_height + randint(-10, 10)
        text = self.write(text, char_font=self.Small_Bold, ink = randink(True))
        self.get_field_coord(text, [text], ["signer_position"], self.Small_Bold)
        
        
        
        # ten nguoi ky
        center_x = self.cursor[0] + self.get_text_length(text, self.Bold) // 2
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
        text = capbac+name
        
        self.cursor[0] = center_x - self.get_text_length(text, self.Bold) // 2 + randint(-80, 80)
        self.cursor[1] = randint(900, 1050)
        text = self.write(text, char_font=self.Bold, ink=randink(True))
        self.get_field_coord(text, [capbac, name], ["signer_rank", "signer_name"], self.Bold)


        # han su dung
        self.cursor[0] = randint(180, 220)
        self.cursor[1] = self.br_poitrait[1] + randint(0, 70)
        text = "Hạn sử dụng:"
        
        text = self.write(text, char_font=self.hsd, ink=randink(True))
        self.get_marker_coord(text, [text], ["marker_expiry"], self.hsd)
        
        # actual hsd
        self.cursor[0] += self.get_text_length(text, self.hsd) + randint(5, 50)
        self.cursor[1] += randint(-10, 10)
        thang = randint(1, 13)
        nam = randint(1000, 3000)
        text = f"{thang}/{nam}"
        
        text = self.write(text, char_font=self.hsd, ink=randink(True))
        self.get_field_coord(text, [text], ["expiry"], self.hsd)

    def fake_glare(self):
        if np.random.rand() > 0.7:
            i = np.random.randint(0, 4)
            for _ in range(i ):
                glare_path = np.random.choice(glob.glob('flare/cmsq_back.png'))
                glare_img = Image.open(glare_path).resize((800, 800))
                self.image = self.image.convert("RGBA")
                glare_img = glare_img.convert("RGBA")
                # random position
                position = (np.random.randint(0, self.img_width - 800), np.random.randint(0, self.img_height - 800))
                self.image.paste(glare_img, position, glare_img)
                self.image = self.image.convert("RGB")
                self.draw = ImageDraw.Draw(self.image)


    def fake_potrait(self):
        offset_x = np.random.randint(-10, 10)
        offset_y = np.random.randint(-3, 2)
        self.tl_poitrait = [158 + offset_x, 445 + offset_y]
        
        glare_path = np.random.choice(
            glob.glob('potrait/*'))
        size = (420 + np.random.randint(-50, 50), 590 + np.random.randint(-50, 50))
        glare_img = Image.open(glare_path).resize(size)
        self.image = self.image.convert("RGBA")
        glare_img = glare_img.convert("RGBA")
        # random position
        position = tuple(self.tl_poitrait)
        self.image.paste(glare_img, position, glare_img)
        self.image = self.image.convert("RGB")
        self.draw = ImageDraw.Draw(self.image)

        self.br_poitrait = [self.tl_poitrait[0] + size[0], self.tl_poitrait[1] + size[1]]
        print("pasted potrait")


    def fake_logo(self):
        offset_x = int(np.random.randint(-20, 20))
        # offset_x = 0
        offset_y = int(np.random.randint(-20, 20))
        # offset_y = 0

        tl = (200+offset_x, 100+offset_y)

        logo_path = np.random.choice(glob.glob("logo/cmsq*.png"))
        logo = Image.open(logo_path).resize((350, 320))
        logo = np.array(logo)

        if logo_path.split("/")[-1] in ["cmsq1.png", "cmsq4.png"]:
            logo = random_rotate(logo, deg_range=10)
            logo = constrast_stretching(logo)
            logo = Image.fromarray(logo.astype(np.uint8)).convert('RGBA')
            self.image  = self.image.convert('RGBA')
            self.image.paste(logo, tl, logo)
        elif logo_path.split("/")[-1] in ["cmsq2.png", "cmsq3.png"]:
            mask = np.any((logo[:,:,:] < 200),axis= -1)
            print('mask shape: ', mask.shape)
            print('logo shape: ', logo.shape)
            logo = random_rotate(logo, deg_range=10)
            logo = constrast_stretching(logo)
            src = np.array(self.image)
            y, x = tl
            src[x:x+logo.shape[0], y:y+logo.shape[1], :][mask] = logo[mask]
            self.image = Image.fromarray(src.astype(np.uint8))
        elif logo_path.split("/")[-1] in ["cmsq5.png"]:
            # initialize the mask
            mask = np.zeros(logo.shape[:2], dtype="uint8")
            # filter out all the greenish pixel
            for i in range(logo.shape[0]):
                for j in range(logo.shape[1]):
                    if logo[i][j][1] > 200:
                        mask[i][j] = 255
            mask = np.logical_not(mask)
            logo = random_rotate(logo, deg_range=10)
            logo = constrast_stretching(logo)
            src = np.array(self.image)
            y, x = tl
            src[x:x+logo.shape[0], y:y+logo.shape[1], :][mask] = logo[mask]
            self.image = Image.fromarray(src.astype(np.uint8))
        
        else:
            # initialize the mask
            mask = np.zeros(logo.shape[:2], dtype="uint8")
            # filter out all the greenish pixel
            for i in range(logo.shape[0]):
                for j in range(logo.shape[1]):
                    if logo[i][j][1] > 141:
                        mask[i][j] = 255
            mask = np.logical_not(mask)
            logo = random_rotate(logo, deg_range=10)
            logo = constrast_stretching(logo)
            src = np.array(self.image)
            y, x = tl
            src[x:x+logo.shape[0], y:y+logo.shape[1], :][mask] = logo[mask]
            self.image = Image.fromarray(src.astype(np.uint8))

        self.image = self.image.convert('RGB')
        self.draw = ImageDraw.Draw(self.image)


    def fake_sign(self):
        # print(self.cursor)
        offset_x = int(np.random.normal(-50,50))
        offset_y = int(np.random.normal(-50,50))

        self.sign_area = [1100 + offset_x,  800 + offset_y, 1500 + offset_x ,  1050 + offset_y]

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
        
        
        if np.random.rand() < 0.5:
            inks = list([[1,1,1] , [1,0,0], [1,0,0],[1,0,0]])
            ink = inks[np.random.randint(len(inks))]
            ink = np.array(ink) * np.random.randint(100)
        else:
            ink = np.array([0, 102, 255])
        print(ink.shape)

        
        signal = mask * ink + src[self.sign_area[1] : self.sign_area[3] , self.sign_area[0] : self.sign_area[2]] * (1-mask)
        src[self.sign_area[1] : self.sign_area[3] , self.sign_area[0] : self.sign_area[2]] =  signal
        self.image = Image.fromarray(src)

    def fake_stamp(self):
        offset_x = int(np.random.randint(-70, 70))
        offset_y = int(np.random.randint(-70, 70))

        self.stamp_area = [1000 + offset_x,  600 + offset_y, 1500 + offset_x ,  1100 + offset_y]

        stamp_path = np.random.choice(glob.glob("stamp/*.png"))

        stamp = cv2.imread(stamp_path)
        stamp = random_rotate(stamp, deg_range=30)
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


    def fake(self):
        self.fake_stamp()
        self.fake_potrait()
        self.fake_logo()
        self.fakeMainInfo()
        if np.random.rand() < 0.4:
            self.fake_BG()
        self.fake_glare()
        self.fake_sign()
        self.fake_blur()
        if np.random.rand() < 0.3:
            self.vien_trang()
        if np.random.rand() < 0.3:
            self.ep_plastic()
        self.fake_general_image()

        
        self.save()



if __name__ == '__main__':
    i=0
    while i<1000:
        print("_______________________________________________________________________________________________________________")
        try:
            faker = CMSQ_FRONT()
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
