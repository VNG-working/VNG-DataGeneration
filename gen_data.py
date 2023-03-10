from common import *
from ast import Sub
from copy import deepcopy
import numpy as np
from time import time
import json
import os
import cv2
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.ImageFilter as ImageFilter
from PIL import ImageEnhance

def mapping(boxes, position):
    '''
    Args: 
        boxes: List boxes of smaller module
        position: (x, y) position where to paste module ==> top-left
    Output: 
        list boxes in larger coordinate space
    Note that function not change order of box in list
    '''
    boxes = np.array(boxes) 
    new_boxes = np.copy(boxes)
    new_boxes[:, 0] = boxes[:, 0] + position[0]
    new_boxes[:, 1] = boxes[:, 1] + position[1]
    return new_boxes

def resize(new_shape, img, boxes):
    new_h, new_w = new_shape
    h, w = img.shape[:2]
    scale_x, scale_y = new_w / h, new_h / h
    new_img = cv2.resize(img, (new_w, new_h))
    if isinstance(boxes, list):
        new_boxes = [[x1*scale_x, y1*scale_y, x2*scale_x, y2*scale_y] for (x1, y1, x2, y2) in boxes]
    else: #numpy array
        new_boxes = np.copy(boxes)
        new_boxes[:, 0] = boxes[:, 0] * scale_x
        new_boxes[:, 1] = boxes[:, 1] * scale_y
        new_boxes = new_boxes.tolist()
    
    return new_img, new_boxes

'''
Giả sử mình có 1 tập các sub-module rồi, làm sao để lắp chúng vào mô đun to ?
Tên và địa chỉ 
Template 1:
Tên -> Địa chỉ 
'''
        
class SubModule:
    def __init__(self, shape = [200, 200], canvas=None, marker_prob = 0.5, 
                 marker_font:ImageFont.truetype = None, content_font:ImageFont.truetype = None,
                 markers = [], content = None, label = None, ink = None):
        self.canvas = Image.fromarray(canvas) if canvas is not None else Image.fromarray(np.full(shape + (3,), 255, dtype=np.uint8))
        self.fields = []
        self.markers = markers
        self.content = content
        self.marker_prob = marker_prob
        self.in_module_position = (0, 0)
        self.marker_font = marker_font
        self.content_font = content_font
        self.cursor = [10, 10]
        self.label = label
        self.draw = ImageDraw.Draw(self.canvas)
        self.ink = ink

    def get_shape(self):
        return self.canvas.shape[:2]
    
    def __call__(self):
        # Random if it has marker or not: 
        
        text = ""
        
        if np.random.random() < self.marker_prob:

            marker_text = np.random.choice(self.markers)
            marker_text = random_space(marker_text)
            marker_text = random_capitalize(marker_text)

            text += marker_text
        
            divider_text = np.random.randint(0, 5) * ' ' + ':' + np.random.randint(0, 5) * ' '

            text += divider_text

            self.write(font = self.marker_font, text=text)
            self.get_field_coord(marker_text, [marker_text], ['marker_' + self.label], self.marker_font)
        
        # actual name
        content_text = np.random.choice(self.content)
        content_text = random_capitalize(content_text)
        content_text = random_space(content_text)


        one_line = True if np.random.rand() < 0.1 or len(content_text.split()) < 3 else False
        if one_line:
            # write account name
            self.cursor[0] += self.marker_font.getsize(text)[0]
            self.write(content_text, self.content_font, bold=np.random.choice([False, True]))
            self.get_field_coord(content_text, [content_text], [self.label], self.content_font)
        else:
            # write account name
            part1, part2 = split_text(content_text)
            ## part 1
            self.cursor[0] += self.marker_font.getsize(text)[0]
            self.cursor[1] += np.random.randint(-5, 2)
            self.write(text=part1, font=self.content_font)
            self.get_field_coord(part1, [part1], [self.label], self.content_font)
            ## part 2
            self.cursor[0] = self.cursor[0] * np.random.uniform(0.8, 1.2)
            self.cursor[1] += self.marker_font.getsize(part1)[1] + np.random.randint(0, 5)
            self.write(text=part2, font=self.content_font)
            self.get_field_coord(part2, [part2], [self.label], self.content_font)
        
        self.canvas = np.asarray(self.canvas)
    
    def resize(self, new_shape):
        boxes = [text['box'] for text in self.fields]
        self.canvas, boxes = resize(new_shape, self.canvas, boxes)
        for i in range(len(boxes)):
            self.fields[i]['box'] = boxes[i]
        self.shape = self.canvas.shape[:2]
        print(self.shape)
    
    def get_part(self, x, y):
        '''
            Get a part of canvas within (0, x) and (0, y) 
        '''
        canvas = self.canvas[:y, :x]
        texts = []
        boxes = [text['box'] for text in self.fields]
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            if x2 < x and y2 < y: # Remove box outside of the ROI
                texts.append(self.fields[i])
        part_submodule = SubModule(canvas=canvas)
        part_submodule.texts = texts
        return part_submodule
    
    def write(self, text: str = None, font = None, bold = None):
            """_summary_

            Args:
                text (list): _description_
                char_font (str, optional): _description_. Defaults to "normal".
                ink (_type_, optional): _description_. Defaults to None.
                bold (bool, optional): _description_. Defaults to False.
                font_size (_type_, optional): _description_. Defaults to None.
                cursor (list, optional): _description_. Defaults to None.
                canvas (np.array, optional): _description_. Defaults to None.

            Raises:
                Exception: _description_
                Exception: _description_

            Returns:
                _type_: _description_
            """

            if self.canvas == None:
                raise Exception("canvas cannot be None")

            if self.ink is None:
                self.ink = randink(bold=bold)

            while self.cursor[0] + self.get_text_length(text = text, font = font)[0] > self.canvas.size[0]:
                text = text[:-1]

            self.draw.text(self.cursor, text=text, font = font, fill=self.ink)
    
    def get_text_length(self, text, font) -> int:
        """_summary_

        Args:
            text (_type_): _description_
            font (ImageFont.truetype, optional): _description_. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            int: _description_
        """
        if font == None:
            raise Exception("font cannot be None")

        return font.getsize(text)

    def get_field_coord(self, text, fields, fields_list=[], font=None, poi=False, cursor=None, block_type='', cut=True):
        """
            text = "Ba Le thi mai linh"
            fields = ["ba", "le thi mai linh"]
            fields_list = ["gender", "transfer_name"]

            text = 'ngày 19 tháng 12 năm 2020'
            fields = ['19', '12', '2020']
            field_list = ['field1', 'field2', 'field3']
        """

        "only for 1 line text"

        if cursor == None:
            cursor = self.cursor
        if font == None:
            font = self.normal
        outlier = text

        idx2search = 0 # idx to start to search for field
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
                    words[idx-1] = words[idx-1] + ' ' + '-' + ' ' + words[idx+1]
                    # remove
                    del words[idx+1]
                    del words[idx]

            if field not in text:
                continue
            else:
                start = text.index(field, idx2search) # idx dau tien cuar field trong text

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

            offset = list(cursor).copy()
            # đưa top-left của text, nội dung và font của text vào => suy ra được bb của text đó
            bb_start = self.draw.textbbox(offset, text[:start], font)  # bb cua phan truoc field

            # bb_end = bb_start + self.get_text_length(field)
            text_bbox = self.draw.textbbox(
                (bb_start[2], cursor[1]), field, font)  # bb cuar field

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
                    (word_bb_start[2], cursor[1]), word, font)  # bb cua word trong field
                
                if True:
                    # prevent loi ra le phai
                    flag_loi_ra_le_phai = False
                    while word_bb[2] - get_last_length(word, font) // 4 > self.canvas.size[0]:
                        flag_loi_ra_le_phai = True
                        print('word hit deleted: ', word)
                        word = word[:-1]

                        word_bb = self.draw.textbbox(
                            (word_bb_start[2], cursor[1]), word, font)  # bb cua word trong field
                    
                    
                    # prevent lot xuong duoi
                    if word_bb[3] - get_text_height(word, font) // 5 > self.canvas.size[1]:
                        continue

                # self.xmax = max(self.xmax, word_bb[2])
                # self.xmin = min(self.xmin, word_bb[0])
                # self.ymax = max(self.ymax, word_bb[3]) 

                # widen box
                xmin, ymin, xmax, ymax = widen_box(word_bb[0], word_bb[1], word_bb[2], word_bb[3], cut=cut, size=self.canvas.size)
                _field = {}
                _field["box"] = [xmin, ymin, xmax, ymax]
                _field["type"] = fields_list[i]
                _field["text"] = u"{}".format(word)
                self.fields.append(_field)

                idx += len(word) + 1

                if flag_loi_ra_le_phai:
                    print('final word: ', word)
                    break

        # print('outlier: ', outlier)
        self.get_outlier_coord(outlier, text, font, cursor=cursor, block_type=block_type)

        return 0
    
    def get_outlier_coord(self, outlier, text, font=None, cursor=None, block_type=''):
        # sau khi get hết các field trong 1 line thì các chữ còn lại là outlier => get outlier
        if cursor == None:
            cursor = self.cursor

        if font is None:
            font = self.normal
        # if font == "Bold":
        lines = outlier.split("\n")
        text_lines = text.split("\n")

        line_tl = list(cursor).copy()
        for i, line in enumerate(lines):
            words = line.split(" ")
            text_line = text_lines[i]

            # print(words)
            idx = 0
            for word in words:
                n = len(word)
                if n == 0 or "-" in word:
                    idx += n
                    continue

                # print(text_line )
                # print(word)

                start = text_line.index(word, idx)

                end = start + n
                text_bb = self.draw.textbbox(
                    cursor, text_line[:start], font)
                # bb_end =  self.get_text_length(text_line[:end] , font)
                # if font == self.Big_Bold:
                #     bb = [line_tl[0] + bb_start - 6 , line_tl[1] - 3 , line_tl[0]  + bb_end,line_tl[1] + line_width + 65]
                # else:
                #     bb = [line_tl[0] + bb_start - 6 , line_tl[1] - 3 , line_tl[0]  + bb_end,line_tl[1] + line_width + 20]

                bb = self.draw.textbbox(
                    (text_bb[2], cursor[1]), word, font)
                # self.draw.rectangle(bb , outline = "blue")
                # self.xmax = max(self.xmax, bb[2])
                # self.xmin = min(self.xmin, bb[0])


                xmin, ymin, xmax, ymax = widen_box(bb[0], bb[1], bb[2], bb[3], size=self.canvas.size)
                _field = {}
                _field["xmin"] = xmin
                _field["ymin"] = ymin
                _field["xmax"] = xmax
                _field["ymax"] = ymax
                _field["type"] = 'outlier'
                _field["text"] = u"{}".format(word)
                _field["block_type"] = block_type
                # print(_field["text"])
                self.fields.append(_field)
                idx += n + 1
            line_tl[0] = 120
            line_tl[1] += 58


class Module:
    def __init__(self, shape=(600, 600), canvas=None):
        self.canvas = canvas if canvas is not None else np.full(shape + (3,), 255, np.uint8)
        self.submodules = []

    def get_shape(self):
        return self.canvas.shape[:2]

    def __paste__(self, submodule:SubModule, position:list):
        '''
            Draw submodule onto module at position where shall be topleft of submodule_box
        '''
        submodule_shape = submodule.get_shape()
        module_shape = self.get_shape()
        x, y = position #top-left
        # Check if position out of module
        assert 0 <= x < module_shape[1], "x axis of position out of bound"
        assert 0 <= y < module_shape[0], "y axis of position out of bound"
        x2 = min(x + submodule_shape[1], module_shape[1])
        y2 = min(y + submodule_shape[0], module_shape[0])

        # If submodule has bigger than x or y or both axis of module
        # We have 2 option: Resize submodule or paste a part of submodule
        if x + submodule_shape[1] > module_shape[1] or y + submodule_shape[0] < module_shape[0]:
            if np.random.random() < 0.5:      #Resize
                print("here")
                submodule.resize((x2-x, y2-y))
            else:       #Get part
                submodule = submodule.get_part(x2, y2)               
        
        # Paste submodule and correct the box coordinate
        self.canvas[y:y2, x:x2] = submodule.canvas
        boxes = [text['box'] for text in submodule.fields]
        print(boxes)
        boxes = mapping(boxes, position)
        for i in range(len(boxes)):
            submodule.texts[i]['box'] = boxes[i]
        submodule.in_module_position = position
        self.submodules.append(submodule)
    
    def __call__(self, submodules:list):
        '''
        Paste all submodules to module
        '''



    def resize(self, new_shape):
        boxes = [text['box'] for text in self.fields]
        self.canvas, boxes = resize(new_shape, self.canvas, boxes)
        for i in range(len(boxes)):
            self.fields[i]['box'] = boxes[i]
        self.shape = self.canvas.shape[:2]

    def get_part(self, x, y):
        '''
            Get a part of canvas within (0, x) and (0, y) 
        '''
        canvas = self.canvas[:y, :x]
        texts = []
        boxes = [text['box'] for text in self.fields]
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            if x2 < x and y2 < y: # Remove box outside of the ROI
                texts.append(self.fields[i])
        part_submodule = SubModule(canvas=canvas)
        part_submodule.fields = texts
        return part_submodule

# ## Below is examples

# class Seller(Module):
#     def __init__(self, size=(600, 600), canvas=None):
#         super().__init__(size, canvas)
    
#     def __call__(self, company_name, company_address, phone, fax, tax,
#                  account_number, represented_name, represented_position,
#                  account_name, bank_name, swift_code):
#         '''
#         Should list all submodule may appear in module for not be missed
#         '''
#         # We already knew that company name and company address always on top
#         # assume
