import os
import unidecode
import numpy as np
import cv2
from PIL import Image, ImageDraw
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageFilter as ImageFilter
from PIL import ImageEnhance
import string
import json
from random import randint

font_scale = 32

normal = ImageFont.truetype(
    os.getcwd() + "/fonts/Arial/ARIAL.ttf", size=font_scale)

hsd = ImageFont.truetype(
    os.getcwd() + "/fonts/Arial/ARIAL.ttf", size=font_scale-20)
bold = ImageFont.truetype(
    os.getcwd() + "/fonts/Arial/ARIALBD.ttf", size=font_scale+randint(-5, 5))
italic = ImageFont.truetype(
    os.getcwd() + "/fonts/Arial/ARIALI.ttf", size=font_scale-10)
big_bold = ImageFont.truetype(
    os.getcwd() + "/fonts/Arial/ARIALBD.ttf", size=font_scale + 10)
Bold_Italic = ImageFont.truetype(
    os.getcwd() + "/fonts/Arial/ARIALBI.ttf", size=font_scale)
code_font = ImageFont.truetype(
    os.getcwd() + "/fonts/Arial/ARIAL.ttf", size=font_scale + 20)

roboto = ImageFont.truetype('fonts/Roboto-Bold.ttf', font_scale + randint(-5, 5))
inhoa_1 = np.random.choice([
    ImageFont.truetype(os.getcwd() + '/fonts/KGNoRegretsSolid.ttf',
                        font_scale+5),
    ImageFont.truetype(
        os.getcwd() + '/fonts/Hand Scribble Sketch Times.otf', font_scale+5)
])

bsx_font = ImageFont.truetype(
    os.getcwd() + '/fonts/Hand Scribble Sketch Times.otf', int(font_scale*2.5))
bsx_font_small = ImageFont.truetype(
    os.getcwd() + '/fonts/Hand Scribble Sketch Times.otf', font_scale+5)

inhoa_2 = np.random.choice([
    ImageFont.truetype(
        os.getcwd() + '/fonts/SourceSerifPro-Semibold.otf', font_scale+5),
    ImageFont.truetype(
        os.getcwd() + '/fonts/DroidSerif-Regular.ttf', font_scale+5),
    ImageFont.truetype(
        os.getcwd() + '/fonts/Times-New-Roman-Bold_44652.ttf', font_scale+5),
])

date2text = {
    '01': 'một',
    '02': 'hai',
    '03': 'ba',
    '04': 'bốn',
    '05': 'năm',
    '06': 'sáu',
    '07': 'bảy',
    '08': 'tám',
    '09': 'chín',
    '10': 'mười',
    '11': 'mười một',
    '12': 'mười hai',
    '13': 'mười ba',
    '14': 'mười bốn',
    '15': 'mười lăm',
    '16': 'mười sáu',
    '17': 'mười bảy',
    '18': 'mười tám',
    '19': 'mười chín',
    '20': 'hai mươi',
    '21': np.random.choice(['hai mươi mốt', 'hai mốt']),
    '22': np.random.choice(['hai mươi hai', 'hai hai']),
    '23': np.random.choice(['hai mươi ba', 'hai ba']),
    '24': np.random.choice(['hai mươi bốn', 'hai bốn']),
    '25': np.random.choice(['hai mươi lăm', 'hai lăm']),
    '26': np.random.choice(['hai mươi sáu', 'hai sáu']),
    '27': np.random.choice(['hai mươi bảy', 'hai bảy']),
    '28': np.random.choice(['hai mươi tám', 'hai tám']),
    '29': np.random.choice(['hai mươi chín', 'hai chín']),
    '30': 'ba mươi',
    '31': np.random.choice(['ba mươi mốt', 'ba mốt']),
}

digit2text = {
    '0': 'không',
    '1': 'một',
    '2': 'hai',
    '3': 'ba',
    '4': 'bốn',
    '5': 'năm',
    '6': 'sáu',
    '7': 'bảy',
    '8': 'tám',
    '9': 'chín',
}

common_words = [
    'chạy',
    'đi',
    'đá',
    'bơi',
    'đi bộ',
    'công chức',
    'công nhân',
    'bố',
    'mẹ',
    'con',
    'chồng',
    'vợ',
    'đàn ông',
    'phụ nữ',
    'người',
    'người ta',
    'người đàn ông',
    'người phụ nữ',
    'người mẹ',
    'người bố',
    'người con',
    'cháu',
    'ông',
    'bà',
    'lại',
    'bản chính',
    'bản gốc',
    'bản thân',
    'bản sao',
    'đi chơi',
    'chúc chích',
    'chúc mừng',
    'lần',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
]

def random_phrase(num_word):
    phrase = ''
    for _ in range(num_word):
        phrase += np.random.choice(common_words) + ' '
    return phrase

def year2text(year):
    assert len(year) == 4, "year must be 4 digits"
    assert year.isdigit(), "year must be digit"

    text = ''

    # year[0]
    if year[0] == '1':
        text += np.random.choice(['một ngàn', 'một nghìn'])
    elif year[0] == '2':
        text += np.random.choice(['hai ngàn', 'hai nghìn'])
    
    if year[1:] == '000':
        return text

    # year[1]
    if year[1] != '0':
        text += ' ' + digit2text[year[1]] + ' trăm'

    # year[2]
    if year[2] == '0':
        text += np.random.choice([' linh', ' lẻ'])
    elif year[2] == '1':
        text += ' mười'
    else:
        text += ' ' + digit2text[year[2]] + np.random.choice([' mươi', ''])
    
    # year[3]
    if year[3] == '0':
        if year[2] == '0':
            # remove last word from text
            text = ' '.join(text.split(' ')[:-1])
    elif year[3] == '1':
        if year[2] == '1' or (year[2]=='0' and year[1]=='0'):
            text += ' một'
        else:
            text += ' mốt'
    elif year[3] == '4':
        text += np.random.choice([' bốn', ' tư'])
    elif year[3] == '5':
        text += 'lăm'
    else:
        text += ' ' + digit2text[year[3]]


    return text


def dob2text(dob):
    date, month, year = dob.split('/')

    date_text = 'Ngày ' + date2text[date] + ', '
    month_text = 'tháng ' + date2text[month] + ', '
    year_text = 'năm ' + year2text(year)

    return date_text + month_text + year_text


def rand_ethnic():
    with open('ethnic_final.txt', 'r') as f:
        lines = f.readlines()
    return np.random.choice(lines)



def remove_accent(text):
    return unidecode.unidecode(text)
    

def randint(a, b):
    return np.random.randint(a, b)

def rand_normal(a, b):
    return np.random.normal(a, b)

def randink(bold=False, extra_bold=False):

    if bold:
        return tuple([int(np.random.normal(30, 10))] * 4)
    
    if extra_bold:
        return tuple([int(np.random.normal(15, 5))] * 4)
        
    return tuple([int(np.random.normal(50, 10))] * 4)

def randink_blue(bold=False):
    if bold:
        return (0, 153, 255)
    ls = [(26, 117, 255), (51, 133, 255), (77, 148, 255), \
                            (0, 92, 230), (51, 102, 255)]
                    
    return ls[randint(0, len(ls))]

def rand_choice(ls):
    return np.random.choice(ls)

def random_number(num_digit):
    number = ''
    for _ in range(num_digit):
        number += str(np.random.randint(0, 10))
    return str(number)

def random_character(num_char, upper='true', number='false'):
    if upper == 'true':
        if number == 'true':
            return ''.join(np.random.choice(list(string.ascii_letters + string.digits), num_char))
        return ''.join(np.random.choice(list(string.ascii_uppercase), num_char))
    elif upper == 'false':
        return ''.join(np.random.choice(list(string.ascii_lowercase), num_char))
    elif upper == 'all':
        special_chars = ['.', '/', ':', '{', '}', '|',  '&',  '(', ')', '-']
        return ''.join(np.random.choice(list(string.ascii_letters) + special_chars, num_char))
    

def rounded_img(img):
    img = Image.fromarray(img)
    w, h = img.size
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    offset = np.random.randint(5, 10)
    draw.rounded_rectangle((offset, offset, img.size[0]-offset, img.size[1]-offset), radius=np.random.randint(10, 20), fill=255)
    img.putalpha(mask)
    return np.array(img)

def ep_plastic(img):
    roi_img = Image.fromarray(img).convert('RGBA')
    roi_w, roi_h = roi_img.size
    pad = min(roi_w, roi_h) // 20
    val = (np.random.randint(200, 255), ) + (np.random.randint(200, 255), ) + (np.random.randint(200, 255), ) + (np.random.randint(80, 120), )
    roi_plastic = Image.new('RGBA', (roi_w+pad*2, roi_h+pad*2), val)
    roi_plastic.paste(roi_img, (pad, pad), roi_img)

    mask = Image.new('L', roi_plastic.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, roi_plastic.size[0], roi_plastic.size[1]), radius=np.random.randint(40, 60), fill=np.random.randint(60, 100))
    draw.rectangle((pad, pad, pad+roi_w, pad+roi_h), fill=255)
    roi_plastic.putalpha(mask)
    final_roi = np.array(roi_plastic)

    return final_roi


def vien_trang(img):
    pad_value = np.random.randint(200, 255)
    pad_size = min(img.shape[:2]) // 20
    padded_roi = cv2.copyMakeBorder(img, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_CONSTANT, value=[pad_value, pad_value, pad_value])
    
    return padded_roi


def random_vn_sentences():
    with open('common_vietnamese_words.txt', 'r') as f:
        lines = f.readlines()
    lines = [line.split('-')[0][:-1] for line in lines]
    
    words = np.random.choice(lines, size=np.random.randint(8, 15), replace=False)
    # capitalize first letter in each word
    words = [word[0].upper() + word[1:] if np.random.rand() < 0.15 else word for word in words]
    return ' '.join(words)

def get_info(path="ds_cty.txt"):
    """
        company_names: list of all company name in the file ds_cty.txt
        names: list of ten cua nguoi dai dien cong ty 
    """
    with open(path, 'r', encoding='utf-8') as f:
        raws = f.read().split('\n')
    raws = [r for r in raws if r != '']
    names = [r.split(':')[-1] for r in raws[1::3]]
    addresses = [r[9:] for r in raws[2::3]]
    
    return names, addresses


def get_brand(path):
    with open(path, 'r') as f:
        brands = f.read().split('\n')
    
    # filter only keep element that has more than one character
    brands = [b for b in brands if len(b) > 1]
    return brands

def get_model_code(path):
    with open(path, 'r') as f:
        codes = f.read().split('\n')
    
    codes = [c for c in codes if not c.startswith('#') and len(c)>1]
    return codes

def correct_address(address):
    ls_remove = ['tỉnh', 'thành phố', 'quận', "huyện", "thị xã", 'đường', 'thị trấn', 'phường']
    address = address.lower()
    for r in ls_remove:
        address = address.replace(r, '')
    
    # title
    address = address.title()

    # remove 2 consecutive space
    address = ' '.join(address.split())
    
    address = address.replace(',,', ',')
    address = address.replace(', ,', ',')
    address = address.replace(' ,', ',')

    return address


def random_rotate(image , deg_range = 15 , border = (255,255,255)):
    d = np.random.randint(-deg_range,deg_range)
    h ,w = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), d, 1.0)
    # print(M)
    rotated = cv2.warpAffine(image, M, (w, h),borderValue = border ) 
    # rotated[rotated < 10 ] = 255
    return rotated 

def constrast_stretching(image):
    min_val = np.min(image)
    max_val = np.max(image)
    return (image - min_val)/(max_val - min_val)  * 255

def noisy(noise_typ,image):
    if noise_typ == "gauss":
        row,col,ch= image.shape
        mean = 0
        var = 3
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = image + gauss
        return noisy

    elif noise_typ == "s&p":
        row,col,ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in image.shape]
        out[coords] = 0
        return out
        
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy
    elif noise_typ =="speckle":
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
        return noisy

def random_date(split='/'):
    # randomly generate a date of birth
    year = np.random.randint(1800, 2100)
    month = np.random.randint(1, 13)
    day = np.random.randint(1, 32)
    return str(day) + '/' + str(month) + '/' + str(year)


import unidecode
import numpy as np
import cv2
from PIL import Image, ImageDraw
import string

date2text = {
    '01': 'một',
    '02': 'hai',
    '03': 'ba',
    '04': 'bốn',
    '05': 'năm',
    '06': 'sáu',
    '07': 'bảy',
    '08': 'tám',
    '09': 'chín',
    '10': 'mười',
    '11': 'mười một',
    '12': 'mười hai',
    '13': 'mười ba',
    '14': 'mười bốn',
    '15': 'mười lăm',
    '16': 'mười sáu',
    '17': 'mười bảy',
    '18': 'mười tám',
    '19': 'mười chín',
    '20': 'hai mươi',
    '21': np.random.choice(['hai mươi mốt', 'hai mốt']),
    '22': np.random.choice(['hai mươi hai', 'hai hai']),
    '23': np.random.choice(['hai mươi ba', 'hai ba']),
    '24': np.random.choice(['hai mươi bốn', 'hai bốn']),
    '25': np.random.choice(['hai mươi lăm', 'hai lăm']),
    '26': np.random.choice(['hai mươi sáu', 'hai sáu']),
    '27': np.random.choice(['hai mươi bảy', 'hai bảy']),
    '28': np.random.choice(['hai mươi tám', 'hai tám']),
    '29': np.random.choice(['hai mươi chín', 'hai chín']),
    '30': 'ba mươi',
    '31': np.random.choice(['ba mươi mốt', 'ba mốt']),
}

digit2text = {
    '0': 'không',
    '1': 'một',
    '2': 'hai',
    '3': 'ba',
    '4': 'bốn',
    '5': 'năm',
    '6': 'sáu',
    '7': 'bảy',
    '8': 'tám',
    '9': 'chín',
}

common_words = [
    'chạy',
    'đi',
    'đá',
    'bơi',
    'đi bộ',
    'công chức',
    'công nhân',
    'bố',
    'mẹ',
    'con',
    'chồng',
    'vợ',
    'đàn ông',
    'phụ nữ',
    'người',
    'người ta',
    'người đàn ông',
    'người phụ nữ',
    'người mẹ',
    'người bố',
    'người con',
    'cháu',
    'ông',
    'bà',
    'lại',
    'bản chính',
    'bản gốc',
    'bản thân',
    'bản sao',
    'đi chơi',
    'chúc chích',
    'chúc mừng',
    'lần',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
]

def random_phrase(num_word):
    phrase = ''
    for _ in range(num_word):
        phrase += np.random.choice(common_words) + ' '
    return phrase

def year2text(year):
    assert len(year) == 4, "year must be 4 digits"
    assert year.isdigit(), "year must be digit"

    text = ''

    # year[0]
    if year[0] == '1':
        text += np.random.choice(['một ngàn', 'một nghìn'])
    elif year[0] == '2':
        text += np.random.choice(['hai ngàn', 'hai nghìn'])
    
    if year[1:] == '000':
        return text

    # year[1]
    if year[1] != '0':
        text += ' ' + digit2text[year[1]] + ' trăm'

    # year[2]
    if year[2] == '0':
        text += np.random.choice([' linh', ' lẻ'])
    elif year[2] == '1':
        text += ' mười'
    else:
        text += ' ' + digit2text[year[2]] + np.random.choice([' mươi', ''])
    
    # year[3]
    if year[3] == '0':
        if year[2] == '0':
            # remove last word from text
            text = ' '.join(text.split(' ')[:-1])
    elif year[3] == '1':
        if year[2] == '1' or (year[2]=='0' and year[1]=='0'):
            text += ' một'
        else:
            text += ' mốt'
    elif year[3] == '4':
        text += np.random.choice([' bốn', ' tư'])
    elif year[3] == '5':
        text += 'lăm'
    else:
        text += ' ' + digit2text[year[3]]


    return text


def dob2text(dob):
    date, month, year = dob.split('/')

    date_text = 'Ngày ' + date2text[date] + ', '
    month_text = 'tháng ' + date2text[month] + ', '
    year_text = 'năm ' + year2text(year)

    return date_text + month_text + year_text


def rand_ethnic():
    with open('ethnic_final.txt', 'r') as f:
        lines = f.readlines()
    return np.random.choice(lines)



def remove_accent(text):
    return unidecode.unidecode(text)
    

def randint(a, b):
    return np.random.randint(a, b)

def rand_normal(a, b):
    return np.random.normal(a, b)

def randink(bold=False, extra_bold=False):

    if bold:
        return tuple([int(np.random.normal(30, 10))] * 4)
    
    if extra_bold:
        return tuple([int(np.random.normal(15, 5))] * 4)
        
    return tuple([int(np.random.normal(50, 10))] * 4)

def randink_blue(bold=False):
    if bold:
        return (0, 153, 255)
    ls = [(26, 117, 255), (51, 133, 255), (77, 148, 255), \
                            (0, 92, 230), (51, 102, 255)]
                    
    return ls[randint(0, len(ls))]

def rand_choice(ls):
    return np.random.choice(ls)

def random_number(num_digit):
    number = ''
    for _ in range(num_digit):
        number += str(np.random.randint(0, 10))
    return str(number)

def random_character(num_char, upper='true', number='false'):
    if upper == 'true':
        if number == 'true':
            return ''.join(np.random.choice(list(string.ascii_letters + string.digits), num_char))
        return ''.join(np.random.choice(list(string.ascii_uppercase), num_char))
    elif upper == 'false':
        return ''.join(np.random.choice(list(string.ascii_lowercase), num_char))
    elif upper == 'all':
        special_chars = ['.', '/', ':', '{', '}', '|',  '&',  '(', ')', '-']
        return ''.join(np.random.choice(list(string.ascii_letters) + special_chars, num_char))
    

def rounded_img(img):
    img = Image.fromarray(img)
    w, h = img.size
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    offset = np.random.randint(5, 10)
    draw.rounded_rectangle((offset, offset, img.size[0]-offset, img.size[1]-offset), radius=np.random.randint(10, 20), fill=255)
    img.putalpha(mask)
    return np.array(img)

def ep_plastic(img):
    roi_img = Image.fromarray(img).convert('RGBA')
    roi_w, roi_h = roi_img.size
    pad = min(roi_w, roi_h) // 20
    val = (np.random.randint(200, 255), ) + (np.random.randint(200, 255), ) + (np.random.randint(200, 255), ) + (np.random.randint(80, 120), )
    roi_plastic = Image.new('RGBA', (roi_w+pad*2, roi_h+pad*2), val)
    roi_plastic.paste(roi_img, (pad, pad), roi_img)

    mask = Image.new('L', roi_plastic.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, roi_plastic.size[0], roi_plastic.size[1]), radius=np.random.randint(40, 60), fill=np.random.randint(60, 100))
    draw.rectangle((pad, pad, pad+roi_w, pad+roi_h), fill=255)
    roi_plastic.putalpha(mask)
    final_roi = np.array(roi_plastic)

    return final_roi


def vien_trang(img):
    pad_value = np.random.randint(200, 255)
    pad_size = min(img.shape[:2]) // 20
    padded_roi = cv2.copyMakeBorder(img, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_CONSTANT, value=[pad_value, pad_value, pad_value])
    
    return padded_roi


def random_vn_sentences():
    with open('common_vietnamese_words.txt', 'r') as f:
        lines = f.readlines()
    lines = [line.split('-')[0][:-1] for line in lines]
    
    words = np.random.choice(lines, size=np.random.randint(8, 15), replace=False)
    # capitalize first letter in each word
    words = [word[0].upper() + word[1:] if np.random.rand() < 0.15 else word for word in words]
    return ' '.join(words)

def get_info(path="ds_cty.txt"):
    """
        company_names: list of all company name in the file ds_cty.txt
        names: list of ten cua nguoi dai dien cong ty 
    """
    with open(path, 'r', encoding='utf-8') as f:
        raws = f.read().split('\n')
    raws = [r for r in raws if r != '']
    names = [r.split(':')[-1] for r in raws[1::3]]
    addresses = [r[9:] for r in raws[2::3]]
    
    return names, addresses


def get_brand(path):
    with open(path, 'r') as f:
        brands = f.read().split('\n')
    
    # filter only keep element that has more than one character
    brands = [b for b in brands if len(b) > 1]
    return brands

def get_model_code(path):
    with open(path, 'r') as f:
        codes = f.read().split('\n')
    
    codes = [c for c in codes if not c.startswith('#') and len(c)>1]
    return codes

def correct_address(address):
    ls_remove = ['tỉnh', 'thành phố', 'quận', "huyện", "thị xã", 'đường', 'thị trấn', 'phường']
    address = address.lower()
    for r in ls_remove:
        address = address.replace(r, '')
    
    # title
    address = address.title()

    # remove 2 consecutive space
    address = ' '.join(address.split())
    
    address = address.replace(',,', ',')
    address = address.replace(', ,', ',')
    address = address.replace(' ,', ',')

    return address


def random_rotate(image , deg_range = 15 , border = (255,255,255)):
    d = np.random.randint(-deg_range,deg_range)
    h ,w = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), d, 1.0)
    # print(M)
    rotated = cv2.warpAffine(image, M, (w, h),borderValue = border ) 
    # rotated[rotated < 10 ] = 255
    return rotated 

def constrast_stretching(image):
    min_val = np.min(image)
    max_val = np.max(image)
    return (image - min_val)/(max_val - min_val)  * 255

def noisy(noise_typ,image):
    if noise_typ == "gauss":
        row,col,ch= image.shape
        mean = 0
        var = 3
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = image + gauss
        return noisy

    elif noise_typ == "s&p":
        row,col,ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in image.shape]
        out[coords] = 0
        return out
        
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy
    elif noise_typ =="speckle":
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
        return noisy

def random_date(split='/'):
    # randomly generate a date of birth
    year = np.random.randint(1800, 2100)
    month = np.random.randint(1, 13)
    day = np.random.randint(1, 32)
    return str(day) + '/' + str(month) + '/' + str(year)


def rotate_bound(image, angle, pts=[[0.01, 0.01], [0.99, 0.01], [0.99, 0.99], [0.01, 0.99]]):
    """
        img: src image
        angle: rotate angle
        pts: coords of four corners of the real roi to paste on background (absolute value)
        roi (rectangular) = real roi (polygon) + zero padding
    """
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image (shape của image sau khi xoay)
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # inverse matrix of simple rotation is reversed rotation.
    M_inv = cv2.getRotationMatrix2D((cX, cY), angle * (-1), 1)
    M_inv[0, 2] += (nW / 2) - cX
    M_inv[1, 2] += (nH / 2) - cY

    # points
    pts = np.array(pts)
    # add ones
    ones = np.ones(shape=(len(pts), 1))
    points_ones = np.hstack([pts, ones])

    # transform points: maxtrix xoay * (coords để paste img trên background)
    transformed_points = M_inv.dot(points_ones.T).T

    # return lại ảnh đã rotate
    return cv2.warpAffine(image, M, (nW, nH), borderValue=(255, 255, 255)), transformed_points
    

def random_capitalize(text):
    # new_text = ''
    # for word in text.split():
    #     type = np.random.choice([1, 2, 3, 4])
    #     if type == 1:
    #         new_text += word.upper() + ' '
    #     elif type == 2:
    #         new_text += word.lower() + ' '
    #     elif type == 3:
    #         new_text += word.title() + ' '
    #     else:
    #         new_text += word + ' '

    # return new_text.strip()

    type = np.random.randint(0, 4)
    if type == 1:
        return text.lower()
    elif type == 2:
        return text.upper()
    elif type == 3:
        return text.title()
    else:
        return text

def random_space(text):
    """
        randomly replace a space in text with 0-5 space
    """
    new_text = ''
    for word in text.split():
        if np.random.randint(0, 2) == 1:
            new_text += word + ' '
        else:
            new_text += word + ' ' * np.random.randint(0, 6)

    return new_text.strip()


def split_text(text, factor=0.5):
    """
        cut text randomly at at least <factor> * text_length index
    """
    lowest = int(factor * len(text))
    split_indices = [idx for idx, c in enumerate(text) if idx > lowest and c == ' ']
    if len(split_indices) == 0:
        return [text]
    else:
        idx = np.random.choice(split_indices)
        return [text[:idx], text[idx+1:]]

def get_last_length(text, font):
    return font.getsize(text[-1])[0]

def get_text_height(text, font=None):    
    max = 0
    for i in range(len(text)):
        if font.getsize(text[i])[1] > max:
            max = font.getsize(text[i])[1]
    
    return max

def widen_box(xmin, ymin, xmax, ymax, factor=1.1, cut=True, size = None):     
    center = [(xmax + xmin) / 2, (ymax + ymin) / 2]
    # print("original" , xmin , ymin , xmax , ymax)
    # print(center)
    xmin = int(1.05 * ( xmin - center[0] ) + center[0])
    xmax = int( 1.03 * ( xmax- center[0] ) + center[0])
    ymin = int(factor * (ymin - center[1]) + center[1])
    ymax = int(factor * (ymax - center[1]) + center[1])

    if cut:
        if xmax > size[0]:
            xmax = size[0]
        if ymax > size[1]:
            ymax = size[1]

    # print(xmin , ymin , xmax , ymax)
    return xmin, ymin, xmax, ymax