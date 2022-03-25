# -*- coding: utf-8 -*-


import xlwt
import random
from datetime import datetime

style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

ws.write(0, 0, "IMEI", style0)
#ws.write(0, 1, "国家", style0)
#ws.write(0, 2, "手机号", style0)
#ws.write(0, 3, "单位", style0)

for j in range(1, 200):
    for i in range(1, 65535, 1):
    
        xing = '0123456789'
        ming = '0123456789'
        x = random.choice(xing)
        m = "".join(random.choice(ming) for i in range(1, 15))
        name = x + m
    
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
        randomPre = random.choice(prelist)
        Number = "".join(random.choice("0123456789") for i in range(8))
        phoneNum = randomPre +Number
    
        ws.write(i, 0, name)
        ws.write(i, 1, "中国大陆")
        ws.write(i, 2, phoneNum)
        ws.write(i, 3, "测试单位")
    else:
        print("循环结束")
    
    wb.save('{}_imei.xls'.format(j))




