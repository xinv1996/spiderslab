# -*- coding:utf-8 -*-
# @author: xrx
# @time: 2023/2/22 15:21
# @project: spiderslab
# @file: qcc.py
# @software: PyCharm
# desc:

import requests


url = 'https://www.qcc.com/api/company/getHotNews?keyNo=f625a5b661058ba5082ca508f99ffe1b'

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "1f0cfff5cd2284c4e94d": "7434bc15cdcf611e8b79b42ea54f838627665eec61ab2b3fb882be7e76f6b80afe9652cb191a30ea1068ea2a858b2ce912cb4eda35863faac67e3662bdce4857",
    "cookie": "acw_tc=1bdd78ad16770483307687786e24deef1c46dcdb3e955fed466d038628; QCCSESSID=5438ebb03870b883685156b4d2; qcc_did=f11dc9bb-dfaa-457b-8be3-016ad7917dff; UM_distinctid=18677dec0f5231-0f0c121fd4bfff-1f525634-1ea000-18677dec0f6b13; CNZZDATA1254842228=1946206699-1677046449-https%253A%252F%252Fwww.baidu.com%252F%7C1677046449",
    "referer": "https://www.qcc.com/web/search?key=%E7%99%BE%E5%BA%A6",
    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "x-pid": "dc835039edc43e0927bf6050da0937c9",
    "x-requested-with": "XMLHttpRequest",
}

response = requests.get(url=url, headers=headers)

print(response.text)
