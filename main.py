# /usr/env/bin/python3
# -*-coding: utf-8 -*-


'la gou wang spider'

__author__ = 'zfyao'
__data__ = '2020-2-16'


import time
import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json


def get_session(url, header):
    s = requests.Session()
    try:
        status_code = s.get(url, headers=header).status_code
        if status_code == 200:
            return s
        return None
    except RequestException:
        print('WRONG!!!')
        return None


def get_json(first_url, second_url, header, form_data):
    s = get_session(first_url, header)
    cookies = s.cookies
    header['Referer'] = first_url
    js = s.post(second_url, data=form_data, headers=header, cookies=cookies).content.decode()
    return json.loads(js)


def parse_json(data):
    results = data['content']['positionResult']['result']
    return results


def get_detail(result):
    return {
        'positionName': result['positionName'],
        'company': result['companyFullName'],
        'industryField': result['industryField'],
        'companyLabelList': result['companyLabelList']
    }


def is_chinese(string):
    for code in string:
        if u'\u4e00' <= code <= u'\u9fa5':
            return string.encode('utf-8').decode('latin-1')
    return string


def main(keyword, city, page_last=2, page_first=1):
    print('>>>>>>>start>>>>>>>')
    form_data = {
        'first': 'true',
        'pn': None,
        'kd': is_chinese(keyword)
    }
    query_data = {
        'city': city,
        'needAddtionalResult': 'false'
    }
    hd = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8'
    }
    html_url = 'https://www.lagou.com/jobs/list_' + keyword
    json_url = 'https://www.lagou.com/jobs/positionAjax.json?' + urlencode(query_data)
    for i in range(page_first, page_last+1):
        print('page_number: %d' % i)
        form_data['pn'] = str(i)
        data = get_json(html_url, json_url, header=hd, form_data=form_data)
        results = parse_json(data)
        for result in results:
            print(get_detail(result))
        time.sleep(2)
    print('>>>>>>>>end>>>>>>>>')


if __name__ == '__main__':
    main('linux', '杭州', 6)