import time
import requests
import config
import os


def get_now_time():
    return int(time.time())


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


# 接口请求
def repeat_request(type, url, headers, json):
    try:
        print('休息%s秒' % (config.sleep_time))
        time.sleep(config.sleep_time)
        if type == 'post':
            return requests.post(url, headers=headers, json=json).json()

        else:
            return requests.get(url)
    except:
        config.sleep_time = config.sleep_time + 0.1
        config.error_sleep_time = config.error_sleep_time + 1
        print('请求异常，休息%s秒！当前接口请求间隔为%s秒,当前错误后休息时间为%s秒。' %
              (config.error_sleep_time, config.sleep_time, config.error_sleep_time))
        time.sleep(config.error_sleep_time)
        return repeat_request(type, url, headers, json)


# 获取请求参数
def get_body(category, offset, size=config.maxSize):
    return {
        "size": size,
        "offset": offset,
        "sortField": "fundnetassets",
        "sortType": "DESC",
        "quoteType": "MUTUALFUND",
        "topOperator": "AND",
        "query": {
            "operator": "AND",
            "operands": [
                {
                    "operator": "or",
                    "operands": [{"operator": "EQ", "operands": ["exchange", "NAS"]}]
                },
                {
                    "operator": "or",
                    "operands": [
                        {"operator": "EQ", "operands": [
                            "categoryname", category]}
                    ]
                }
            ]
        },
        "userId": "",
        "userIdType": "guid"
    }


# 请求接口
def get_fund_name_list_requrst(category):
    url = 'https://query1.finance.yahoo.com/v1/finance/screener?crumb=FVRuE%2F%2FRA0j&lang=en-US&region=US&formatted=true&corsDomain=finance.yahoo.com'
    headers = {'authority': 'query1.finance.yahoo.com',
               'pragma': 'no-cache',
               'cache-control': 'no-cache',
               'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
               'sec-ch-ua-mobile': '?0',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
               'content-type': 'application/json',
               'accept': '*/*',
               'origin': 'https://finance.yahoo.com',
               'sec-fetch-site': 'same-site',
               'sec-fetch-mode': 'cors',
               'sec-fetch-dest': 'empty',
               'referer': 'https://finance.yahoo.com/screener/mutualfund/new',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
               'cookie': 'APID=UP0d4f041a-9f34-11eb-941f-02abf34d1af2; B=60b8u75g7dldj&b=3&s=ua; GUC=AQEBAQFgeCdggEIaPAQe; A1=d=AQABBLPVdmACEHep_YUpegS2PhLZ2DkeLWAFEgEBAQEneGCAYAAAAAAA_eMAAAcIs9V2YDkeLWA&S=AQAAAv8-Uq0nI5LAUD_QyOs8cCE; A3=d=AQABBLPVdmACEHep_YUpegS2PhLZ2DkeLWAFEgEBAQEneGCAYAAAAAAA_eMAAAcIs9V2YDkeLWA&S=AQAAAv8-Uq0nI5LAUD_QyOs8cCE; A1S=d=AQABBLPVdmACEHep_YUpegS2PhLZ2DkeLWAFEgEBAQEneGCAYAAAAAAA_eMAAAcIs9V2YDkeLWA&S=AQAAAv8-Uq0nI5LAUD_QyOs8cCE&j=WORLD; cmp=t=1618822351&j=0; APIDTS=1618822359; PRF=t%3DWABIX%252BXISC.JK%252B0P0000VTOL.BO%252B%255EGSPC'}

    params = {
        "crumb": "FVRuE%2F%2FRA0j",
        "lang": "en-US",
        "region": "US",
        "formatted": "true",
        "corsDomain": "finance.yahoo.com"
    }

    body = get_body(category, 0)

    time.sleep(config.sleep_time)

    first_request = repeat_request('post', url, headers=headers, json=body)

    total = first_request['finance']['result'][0]['total']

    fund_name_list = []

    for i in range(len(first_request['finance']['result'][0]['quotes'])):
        fund_name_list.append(
            first_request['finance']['result'][0]['quotes'][i]['symbol'])

    print(total)

    if total <= config.maxSize:
        return fund_name_list
    else:
        for_count = total // config.maxSize
        for i in range(for_count):
            for_body = get_body(category, (i + 1) * config.maxSize)

            for_request = repeat_request(
                'post', url, headers=headers, json=for_body)

            for j in range(len(for_request['finance']['result'][0]['quotes'])):
                fund_name_list.append(
                    for_request['finance']['result'][0]['quotes'][j]['symbol'])
        return fund_name_list


def get_excel(category, fund_name):
    # interval_list = ['1mo', '1wk', '1d']
    interval_list = ['1mo', '1wk']
    start_time = 0
    end_time = get_now_time()

    for i in range(len(interval_list)):
        mkdir('%s/%s' % (category, interval_list[i]))
        url = 'https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=%s&events=history&includeAdjustedClose=true' % (
            fund_name, start_time, end_time, interval_list[i])

        request = repeat_request('get', url, headers={}, json={})

        file_name = "%s/%s/%s-%s-%s.csv" % (category,
                                            interval_list[i], fund_name,  start_time, end_time)
        print(file_name)
        with open(file_name, "wb") as code:
            code.write(request.content)
