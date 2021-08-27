# -*- coding:utf-8 -*-
# @time: 2021/4/19 10:21 上午
# @project: spiderslab 
# @file: main.py
# @software: GoLand
# @desc: https://www.aqistudy.cn/historydata/
import execjs
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.aqistudy.cn",
    "Referer": "https://www.aqistudy.cn/historydata/daydata.php?city=%E4%BF%9D%E5%AE%9A&month=202010",
}
with open('./airHistory.js', 'r',encoding='utf-8') as f:
    js_code = f.read()

js = execjs.compile(js_code)

url = "https://www.aqistudy.cn/historydata/api/historyapi.php"

city = '德州'
# 月统计
# form_data = {"hoAHCQ2cH": js.call("get_req", "GETMONTHDATA", {"city": city})}
# 日统计
# form_data = {"hmebd5PRa": js.call("get_req", "GETDAYDATA",{"city": city, "month": '201409'})}
form_data = {"hGrEW6dcs": "GGQmSXluPKCUewlCorSQeXfE94PIHRAjZOwZwErkNeli4HdcBU98anjVz3dzUxAYNZatMHYkcav27zuP37wvVOW++Nq02K6N3YkAInYziMn2b0ff7c5Nfz8zgddqtRigRbXdeYMlH9a+XNEMF3ZsvjU/kfWqFBisoTeoXBp5UEPinHidMwlDu6EH0LYCvZT2OhVSoK+DSKgQuU6Ra1epypKeY2uPDqYrbu1M+e5DayOA3Sv2/qfYvWKTUtC37pxmv5IKw2L1hvPl3N//9vUPypXPQXF11xMNHOMgxC3XwHrzhwxuWyeOkSUSbtlVRcVhjV1+ydMu4ShcnE7QBH4q/jmTTkidf+NFvK5T4Z/mMM4="}

resp = requests.post(url=url, headers=headers, data=form_data)


print(resp.text)
# res_data = js.call('get_res', resp.text)
#
# print(res_data)
