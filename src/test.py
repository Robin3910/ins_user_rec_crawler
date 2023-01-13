
from urllib.request import urlretrieve
import os
import openpyxl
from openpyxl.drawing.image import Image
from time import time, sleep, localtime

workbook = openpyxl.Workbook()
sheet = workbook.active
img = Image('./imgs/chaii.blog.jpg')
sheet.add_image(img, f'F1')
sheet.column_dimensions['F'].width = img.width
sheet.row_dimensions['1'].height = img.height
workbook.save('userinfo_' + str(time()) + '.xlsx')
