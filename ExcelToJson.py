#*-* coding:utf-8 *-*
import sys
import xlrd
from collections import OrderedDict
import json
import time
from datetime import datetime
from xlrd import xldate_as_tuple
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

wb = xlrd.open_workbook('json.xlsx',formatting_info=False)

xlrd.Book.encoding = "gbk"
convert_list = []
sh = wb.sheet_by_index(0)
title = sh.row_values(0)
for rownum in range(1, sh.nrows):
    rowvalue = sh.row_values(rownum)
    single = OrderedDict()
    for colnum in range(0, len(rowvalue)):
        #print(type(title[colnum]), type(rowvalue[colnum]))
        if type(rowvalue[colnum]) ==  float:
            date = datetime(*xldate_as_tuple(rowvalue[colnum], 0))
            rowvalue[colnum] = date.strftime('%Y-%d-%m %H:%M:%S')
            rowvalue[colnum]=int(time.mktime(time.strptime(rowvalue[colnum], '%Y-%d-%m %H:%M:%S'))*1000)
        single[title[colnum]] = rowvalue[colnum]
    convert_list.append(single)
jsonresult={}
jsonresult["rows"]=convert_list
j = json.dumps(jsonresult,ensure_ascii=False)

#with open('json.txt','wb') as f:
#    f.write(j)
#    f.close()
