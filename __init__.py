import config
import requests
import time
import tool

for i in range(len(config.categoryList)):
    time.sleep(1)
    print('当前类别为：%s' % (config.categoryList[i]))
    fund_name_list = tool.get_fund_name_list_requrst(config.categoryList[i])
    for j in range(len(fund_name_list)):
        tool.get_excel(config.categoryList[i], fund_name_list[j])
        print('%s：[%s/%s]' % (config.categoryList[i], j, len(fund_name_list)))
