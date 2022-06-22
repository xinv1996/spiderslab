# -*- coding:utf-8 -*-
# @project: spiderslab
# @file: main.py
# @software: GoLand

import base64
import time
import datetime

import execjs
import requests


jscode = '''function o() {
    return unescape("861831832863830866861836861862839831831839862863839830865834861863837837830830837839836861835833".replace(/8/g, "%u00"))
}
function i() {
    var e = "";
    return ["66", "72", "6f", "6d", "43", "68", "61", "72", "43", "6f", "64", "65"].forEach(function(t) {
        e += unescape("%u00" + t)
    }),
        e
}
function r(e) {
    var t = i();
    return String[t](e)
}

function f(e, t) {
    t || (t = o()),
    e = e.split("");
    var array=new Array(e.length)

    for (var n = e.length, a = t.length, i = "charCodeAt", s = 0; s < n; s++)
        array[s]=  r(e[s][i](0) ^ t[(s + 10) % a][i](0))
    return array.join("");

}

function get_data(s1){
    s2 = '0000000c735d856'
    return f(s1,s2)
}
'''

# jscode = open('qm.js', 'r').read()
js = execjs.compile(jscode)

url = "https://api.qimai.cn/rank/indexPlus/brand_id/1"

# 参数
# brand: all  country: cn   device: iphone  genre: 36  date: 2021-02-01  page: 3
today = str(datetime.datetime.today()).split()[0]

page = 3

params = ['all', 'cn', 'iphone', '36', today, str(page)]

r = ''.join(sorted(params))
print(f"r:{r}")

base64_r = base64.b64encode(r.encode('utf-8')).decode('utf-8')
print(f"base64_r:{base64_r}")

base_url = 'https://api.qimai.cn'

timestamp = int(time.time() * 1000 - 1515125653845)

_ = '@#'

str_r = base64_r + _ + url + _ + str(timestamp) + _ + '1'
str_r = str_r.replace(base_url, '')
print(f"str_r:{str_r}")
an = js.call('get_data', str_r)

analysis = base64.b64encode(an.encode('utf-8')).decode('utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}

req_params = {
    "analysis": analysis,
    "brand": "all",
    "country": "cn",
    "device": "iphone",
    "genre": "36",
    "date": today,
    "page": page
}

print(req_params)
req = requests.get(url=url, params=req_params, headers=headers)

print(req.text)
