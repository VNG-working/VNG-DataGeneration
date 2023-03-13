import cv2
import numpy as np
from copy import deepcopy

def intersec_over_area_B(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    # boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    # iou = interArea / float(boxAArea + boxBArea - interArea)
    ioaa = interArea / boxBArea
    return ioaa

def is_too_overlap(check_box, boxes, ratio=0.75):
    for box in boxes:
        if intersec_over_area_B(check_box, box) > ratio:
            return True
    return False

def blend(item_src, item_dst):
    '''
    item_src, item_dst: a dictionary with {'img':..., 'boxes':..., 'class_ids':...}
    '''

    item_res = {'boxes':deepcopy(item_dst['boxes']), 'class_ids':deepcopy(item_dst['class_ids'])}
    img = item_dst['img'].copy()
    h, w = img.shape[:2]
    flag = False # check if at least one box can be blended
    for box, name in zip(item_src['boxes'], item_src['class_ids']):
        x1, y1, x2, y2 = [int(b) for b in box]
        roi = item_src['img'][y1:y2, x1:x2]
        hr, wr = roi.shape[:2]
        loop = 0
        while loop < 10: # Try 10 times
            xmin = np.random.randint(w-wr)
            xmax = xmin + wr
            cx = (xmin+xmax)//2
            ymin = np.random.randint(h-hr)
            ymax = ymin + hr
            cy = (ymin+ymax)//2
            if not is_too_overlap([xmin, ymin, xmax, ymax], item_dst['boxes'], ratio=0.5):
                break
            loop += 1
        if loop == 10: # Cannot be blended with current box, move to next box 
            continue
        flag = True
        img = cv2.seamlessClone(roi, img, mask=None, p=(cx, cy), flags=cv2.MONOCHROME_TRANSFER)
        item_res['boxes'].append([xmin, ymin, xmax, ymax])
        item_res['class_ids'].append(name)
    if not flag: #No source box can be blened into destination image --> return source item
        return item_src

    item_res['img'] = img
    return item_res

if __name__ == '__main__':
    import os
    import xml.etree.ElementTree as ET
    from time import time

    def parse_xml(xml):
        root = ET.parse(xml).getroot()
        objs = root.findall('object')
        boxes, ymins, obj_names = [], [], []
        for obj in objs:
            obj_name = obj.find('name').text
            box = obj.find('bndbox')
            xmin = float(box.find('xmin').text)
            ymin = float(box.find('ymin').text)
            xmax = float(box.find('xmax').text)
            ymax = float(box.find('ymax').text)
            ymins.append(ymin)
            boxes.append([xmin, ymin, xmax, ymax])
            obj_names.append(obj_name)
        indices = np.argsort(ymins)
        boxes = [boxes[i] for i in indices]
        obj_names = [obj_names[i] for i in indices]
        return boxes, obj_names

    def resize(image, boxes, size):
        w, h = size
        ih, iw = image.shape[:2]
        scale_w, scale_h = w/iw, h/ih
        new_image = cv2.resize(image, (w, h))
        new_boxes = []
        for box in boxes:
            xmin, ymin, xmax, ymax = box[:4]
            xmin, xmax = int(xmin*scale_w), int(xmax*scale_w)
            ymin, ymax = int(ymin*scale_h), int(ymax*scale_h)
            new_boxes.append([xmin, ymin, xmax, ymax, box[4]])
        return new_image, new_boxes
             
    def show(image, boxes, name='im'):
        for box in boxes:
            xmin, ymin, xmax, ymax = [int(p) for p in box[:4]]
            label = box[4]
            ret, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
            cv2.rectangle(image, (xmin, ymax - ret[1] - baseline), (xmin + ret[0], ymax), (0, 255, 0), -1)
            cv2.putText(image, label, (xmin, ymax - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        cv2.imshow(name, image)

    im_path = r"D:\VNG\E2EObjectDetection\PolypsSet\train2019\Image"
    lb_path = r"D:\VNG\E2EObjectDetection\PolypsSet\train2019\Annotation"
    
    data = [{'fp':os.path.join(im_path, name), 'xp':os.path.join(lb_path, name[:-3]+'xml')} for name in os.listdir(im_path)]
    data = [d for d in data if os.path.exists(d['xp'])]
    for i in range(5):
        d1, d2 = np.random.choice(data, 2)
        img_1 = cv2.imread(d1['fp'])
        boxes_1, names_1 = parse_xml(d1['xp'])

        img_2 = cv2.imread(d2['fp'])
        boxes_2, names_2 = parse_xml(d2['xp'])

        item_res = blend({'img':img_1, 'boxes':boxes_1, 'class_ids':names_1},
                        {'img':img_2, 'boxes':boxes_2, 'class_ids':names_2}  )
        
        boxes_2 = [box + [c] for box, c in zip(boxes_2, names_2)]
        show(img_2, boxes_2, 'img_dst')

        boxes_1 = [box + [c] for box, c in zip(boxes_1, names_1)]
        show(img_1, boxes_1, 'img_source')

        show(item_res['img'], [box + [c] for box, c in zip(item_res['boxes'], item_res['class_ids'])], 'img_result')

        key = cv2.waitKey(0)
        if key == ord('q'):
            exit()
