# -*- coding:utf-8 -*-
# @author: xrx
# @time: 2021/2/20 4:43 下午
# @project: spiderslab 
# @file: main.py
# @software: GoLand
# @desc:

import hashlib

import execjs
import requests

js_code = '''function r_func(e) {
    var t = "06aa4e45fb0d8d20cbc5e611156c7df4"
        , r = "" + (new Date).getTime()
        , i = r + parseInt(10 * Math.random(), 10);
    return {
        ts: r,
        bv: t,
        salt: i,
        sign: "fanyideskweb" + e + i + "Tbh5E8=q6U3EXe+&L[4c@"
    }
};
'''

word = '您好'
js = execjs.compile(js_code)

res_data = js.call('r_func', word)

url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

data = {
    "i": word,
    "from": "AUTO",
    "to": "AUTO",
    "smartresult": "dict",
    "client": "fanyideskweb",
    "salt": str(res_data['salt']),
    "sign": str(hashlib.md5(res_data['sign'].encode('utf-8')).hexdigest()),
    "lts": str(res_data['ts']),
    "bv": str(res_data['bv']),
    "doctype": "json",
    "version": "2.1",
    "keyfrom": "fanyi.web",
    "action": "FY_BY_REALTlME",
}

headers = {
    "Cookie": "OUTFOX_SEARCH_USER_ID=1513811869@123.213.212.123;",
    "Referer": "http://fanyi.youdao.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}

req = requests.post(url=url, headers=headers, data=data)

print(req.text)
