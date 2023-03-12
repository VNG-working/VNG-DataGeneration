import PIL.ImageFont as ImageFont

font_scale = 10

normal = ImageFont.truetype(
    "fonts/time_new_roman.ttf", size=font_scale)
big = ImageFont.truetype(
    "fonts/time_new_roman.ttf", size=font_scale+5)
small = ImageFont.truetype(
    "fonts/time_new_roman.ttf", size=font_scale-2)
extra_big = ImageFont.truetype(
    "fonts/time_new_roman.ttf", size=font_scale+10)

bold = ImageFont.truetype(
    "fonts/Times-New-Roman-Bold_44652.ttf", size=font_scale)
italic = ImageFont.truetype(
    "fonts/Times-New-Roman-Italic_44665.ttf", size=font_scale)
bold_italic = ImageFont.truetype(
    'fonts/Times-New-Roman-Bold-Italic_44651.ttf', font_scale+5)
big_bold = ImageFont.truetype( 
    "fonts/Times-New-Roman-Bold_44652.ttf", size=font_scale + 3)
extra_big_bold = ImageFont.truetype( \
    "fonts/Times-New-Roman-Bold_44652.ttf", size=font_scale + 25)
extra_small = ImageFont.truetype(
    "fonts/time_new_roman.ttf", size=font_scale-7)