from gen_data import *
from common import *
import cv2 as cv

class Contract_Name(SubModule):

    def __init__(self, size=None, canvas=None, marker_prob=0.5, marker_font: ImageFont.truetype = None, 
                 content_font: ImageFont.truetype = None, markers=None, content=None, label=None):
        super().__init__(size, canvas, marker_prob, marker_font, content_font, markers, content, label)    

if __name__ == "__main__":
    test = Contract_Name(size = (2000, 100), marker_font=normal, content_font=normal, 
                         marker_prob=0.8, markers=["A", "B"], content=dc_lst, label="contract_name")

    test()

    cv.imshow("test", test.canvas)
    cv.waitKey(0)