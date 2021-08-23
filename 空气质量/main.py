# -*- coding:utf-8 -*-
# @time: 2021/4/19 10:21 上午
# @project: spiderslab 
# @file: main.py
# @software: GoLand
# @desc: https://www.aqistudy.cn/historydata/
import execjs
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
}
with open('./airHistory_2108.js', 'r') as f:
    js_code = f.read()

js = execjs.compile(js_code)

url = "https://www.aqistudy.cn/historydata/api/historyapi.php"

city = '济南'
# 月统计
form_data = {"hmebd5PRa": js.call("get_req", "GETMONTHDATA", {"city": city})}
# 日统计
# form_data = {"hmebd5PRa": js.call("get_req", "GETDAYDATA",{"city": city, "month": '201409'})}

resp = requests.post(url=url, headers=headers, data=form_data)

res_data = js.call('get_res', resp.text)

print(res_data)
