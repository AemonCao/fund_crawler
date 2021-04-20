import csv
import os
import xlwt
import config
import tool
import logging
import time


def read_csv(csv_path):
    csvFile = open(csv_path, 'r')
    reader = csv.reader(csvFile)

    result = {}
    for item in reader:
        if reader.line_num == 1:
            continue
        result[item[0]] = item[5]

    csvFile.close()
    return result


def new_excel():
    source_path = 'Source'
    date_type = 'mo'
    g = os.walk(source_path)
    # path,dir_list,file_list

    for i, val in enumerate(g):
        if i == 0:
            # 获取类别列表
            dirCategoryList = val[1]

    wordbook = xlwt.Workbook(encoding='utf-8')
    # 类别循环
    for sheet_name in dirCategoryList:
        # 新建 sheet
        sheet = wordbook.add_sheet(sheet_name)
        sheet.write(0, 0, sheet_name)
        category_path = '%s\\%s\\1%s' % (source_path, sheet_name, date_type)
        category_path_g = os.walk(category_path)
        for path, dir_list, file_list in category_path_g:
            logging.info(file_list)

    wordbook.save('D:\\Code\\Python\\fund_crawler\\finally-%s-%s.xls' %
                  (date_type, tool.get_now_time()))


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s \tFile \'%(filename)s\'[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='./' + time.strftime('%Y-%m-%d',
                                  time.localtime(time.time())) + '.log',
    filemode='a')


new_excel()

# source_path = 'Source'

# g = os.walk(source_path)
# # path,dir_list,file_list

# for i, val in enumerate(g):
#     if i == 0:
#         dirCategoryList = val[1]
#     print(val[2])


# print(read_csv('D:\\Code\\Python\\fund_crawler\\Source\\Commodities Broad Basket\\1mo\\ARCIX-0-1618869825.csv'))
