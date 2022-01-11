import base64
import json
import re
import time
import hashlib
from urllib.parse import urljoin

import execjs
import requests


def des_js(js_str):
    keys = re.findall(f'DES\.encrypt\((\w+)\s?,\s?(\w+)\s?,\s?(\w+)\)', js_str)
    text_name, key_name, iv_name = keys[0]
    key = re.findall(f'const\s+?{key_name}\s+?=.*?"(.*?)"', js_str)[0]
    iv = re.findall(f'const\s+?{iv_name}\s+?=.*?"(.*?)"', js_str)[0]
    appid_name = re.findall("appId:.*?(\w+),", js_str)[0]
    appId = re.findall(f"var\s?{appid_name}\s?=.*?'(.*?)'", js_str)[0]
    param_name = re.findall("data:\s?\{\s?(\w+):.*?}", js_str)[0]

    des_keys = re.findall(f'DES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    des_dec_key_name, des_dec_iv_name = des_keys[0]

    des_dec_key = re.findall(f'const\s+?{des_dec_key_name}\s+?=.*?"(.*?)"', js_str)[0]
    des_dec_iv = re.findall(f'const\s+?{des_dec_iv_name}\s+?=.*?"(.*?)"', js_str)[0]

    aes_keys = re.findall(f'AES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    aes_dec_key_name, aes_dec_iv_name = aes_keys[0]
    aes_dec_key = re.findall(f'const\s+?{aes_dec_key_name}\s+?=.*?"(.*?)"', js_str)[0]
    aes_dec_iv = re.findall(f'const\s+?{aes_dec_iv_name}\s+?=.*?"(.*?)"', js_str)[0]

    method = "GETDAYDATA"
    obj = {"city": "济南", "month": '201702'}
    timestamp = int(time.time() * 1000)
    clienttype = 'WEB'
    form_data = {
        "appId": appId,
        "method": method,
        "timestamp": timestamp,
        "clienttype": clienttype,
        "object": obj,
        "secret": hashlib.md5(
            f'{appId}{method}{timestamp}{clienttype}{str(obj)}'.replace("'", '"').replace(' ', '').encode(
                'utf-8')).hexdigest()
    }

    base64_d = base64.b64encode(str(form_data).replace("'", '"').replace(' ', '').encode('utf-8')).decode('utf-8')

    result = js.call("des_encrypt", base64_d, key, iv)
    print(data := {param_name: result})

    url = "https://www.aqistudy.cn/historydata/api/historyapi.php"

    resp = requests.post(url=url, headers=headers, data=data)

    print(resp.text)
    dec_data = js.call('dec_func', resp.text, des_dec_key, des_dec_iv, aes_dec_key, aes_dec_iv)
    print(json.loads(dec_data))


def aes_js(js_str):
    keys = re.findall(f'AES\.encrypt\((\w+)\s?,\s?(\w+)\s?,\s?(\w+)\)', js_str)
    text_name, key_name, iv_name = keys[1]
    key = re.findall(f'const\s+?{key_name}\s+?=.*?"(.*?)"', js_str)[0]
    iv = re.findall(f'const\s+?{iv_name}\s+?=.*?"(.*?)"', js_str)[0]
    appid_name = re.findall("appId:.*?(\w+),", js_str)[0]
    appId = re.findall(f"var\s?{appid_name}\s?=.*?'(.*?)'", js_str)[0]
    param_name = re.findall("data:\s?\{\s?(\w+):.*?}", js_str)[0]

    des_keys = re.findall(f'DES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    des_dec_key_name, des_dec_iv_name = des_keys[0]

    des_dec_key = re.findall(f'const\s+?{des_dec_key_name}\s+?=.*?"(.*?)"', js_str)[0]
    des_dec_iv = re.findall(f'const\s+?{des_dec_iv_name}\s+?=.*?"(.*?)"', js_str)[0]

    aes_keys = re.findall(f'AES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    aes_dec_key_name, aes_dec_iv_name = aes_keys[0]
    aes_dec_key = re.findall(f'const\s+?{aes_dec_key_name}\s+?=.*?"(.*?)"', js_str)[0]
    aes_dec_iv = re.findall(f'const\s+?{aes_dec_iv_name}\s+?=.*?"(.*?)"', js_str)[0]

    method = "GETDAYDATA"
    obj = {"city": "济南", "month": '201702'}
    timestamp = int(time.time() * 1000)
    clienttype = 'WEB'
    form_data = {
        "appId": appId,
        "method": method,
        "timestamp": timestamp,
        "clienttype": clienttype,
        "object": obj,
        "secret": hashlib.md5(
            f'{appId}{method}{timestamp}{clienttype}{str(obj)}'.replace("'", '"').replace(' ', '').encode(
                'utf-8')).hexdigest()
    }

    base64_d = base64.b64encode(str(form_data).replace("'", '"').replace(' ', '').encode('utf-8')).decode('utf-8')

    result = js.call("aes_encrypt", base64_d, key, iv)
    print(data := {param_name: result})

    url = "https://www.aqistudy.cn/historydata/api/historyapi.php"

    resp = requests.post(url=url, headers=headers, data=data)

    dec_data = js.call('dec_func', resp.text, des_dec_key, des_dec_iv, aes_dec_key, aes_dec_iv)
    print(json.loads(dec_data))


def bs64_js(js_str):
    appid_name = re.findall("appId:.*?(\w+),", js_str)[0]
    appId = re.findall(f"var\s?{appid_name}\s?=.*?'(.*?)'", js_str)[0]
    param_name = re.findall("data:\s?\{\s?(\w+):.*?}", js_str)[0]

    method = "GETDAYDATA"
    obj = {"city": "济南", "month": '202112'}
    timestamp = int(time.time() * 1000)
    clienttype = 'WEB'
    form_data = {
        "appId": appId,
        "method": method,
        "timestamp": timestamp,
        "clienttype": clienttype,
        "object": obj,
        "secret": hashlib.md5(
            f'{appId}{method}{timestamp}{clienttype}{str(obj)}'.replace("'", '"').replace(' ', '').encode(
                'utf-8')).hexdigest()
    }

    base64_d = base64.b64encode(str(form_data).replace("'", '"').replace(' ', '').encode('utf-8')).decode('utf-8')

    print(data := {param_name: base64_d})

    url = "https://www.aqistudy.cn/historydata/api/historyapi.php"

    resp = requests.post(url=url, headers=headers, data=data)

    des_keys = re.findall(f'DES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    des_dec_key_name, des_dec_iv_name = des_keys[0]

    des_dec_key = re.findall(f'const\s+?{des_dec_key_name}\s?=.*?"(.*?)"', js_str)[0]
    des_dec_iv = re.findall(f'const\s+?{des_dec_iv_name}\s?=.*?"(.*?)"', js_str)[0]

    aes_keys = re.findall(f'AES\.decrypt\(data,\s?(\w+),\s?(\w+)\);', js_str)
    aes_dec_key_name, aes_dec_iv_name = aes_keys[0]
    aes_dec_key = re.findall(f'const\s+?{aes_dec_key_name}\s?=.*?"(.*?)"', js_str)[0]
    aes_dec_iv = re.findall(f'const\s+?{aes_dec_iv_name}\s?=.*?"(.*?)"', js_str)[0]

    dec_data = js.call('dec_func', resp.text, des_dec_key, des_dec_iv, aes_dec_key, aes_dec_iv)
    print(json.loads(dec_data))


if __name__ == '__main__':
    url = "https://www.aqistudy.cn/historydata/daydata.php?city=%E4%BF%9D%E5%AE%9A&month=201910"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.aqistudy.cn",
        "Referer": "https://www.aqistudy.cn/historydata/daydata.php?city=%E4%BF%9D%E5%AE%9A&month=202009",
    }
    req = requests.get(url, headers=headers)
    js_url = re.findall(r'src="(resource/js/.*?.min.js\?v=\d+)"', req.text)[0]
    js_req = requests.get(url=urljoin(url, js_url), headers=headers)
    print(js_req.url)

    js_code = open('airHistory_2108.js', 'r').read()
    js_bs64_bs64_code = js_req.text[5:-2]
    js_code = js_code.replace('jscode_pattern', js_bs64_bs64_code)
    js = execjs.compile(js_code)
    res = js.call("get_full_js", js_bs64_bs64_code)
    # print(res)
    type_len = len(re.findall("dweklxde", res))
    print(type_len)
    base64_str = re.findall("'(.*?)'", res)[0]
    if type_len == 2:
        target_js = base64.b64decode(base64.b64decode(base64_str)).decode('utf-8')
        des_js(js_str=target_js)
    elif type_len == 1:
        target_js = base64.b64decode(base64_str).decode('utf-8')
        aes_js(js_str=target_js)
    elif type_len == 0:
        bs64_js(js_str=res)
