# -*- coding:utf-8 -*-
# @time: 2021/2/24 2:38 下午
# @project: spiderslab 
# @file: main.py
# @software: GoLand
# @desc: https://www.caasbuy.com/login#/ 科研物资采购平台登录js
import base64
import time
from io import BytesIO

import execjs
import requests
from PIL import Image

js_code = '''
function get_x_auth_token() {
    var UUID = require('uuidjs');
    return UUID.generate()
}


function get_sign(urlstr) {
    # var bcrypt = require('bcrypt');   # mac
    var bcrypt = require('bcryptjs');   # windows
    var r = urlstr.replace('https://www.caasbuy.com','')
    var c = 1e4 * Date.now() + Math.floor(1e4 * Math.random());
    sign = bcrypt.hashSync("requestNonce=".concat(c, "&requestUrl=").concat(r), bcrypt.genSaltSync())
    return {'sign':sign,'nonce':c}
}

function get_passwd(i,aes_key) {
    var crypto = require('crypto-js');
    var r = aes_key
    var a = crypto.enc.Utf8.parse(r)
        , s = crypto.enc.Utf8.parse(i)
        , c = crypto.AES.encrypt(s, a, {
        mode: crypto.mode.ECB,
        padding: crypto.pad.Pkcs7
    })

    return {'password': c.toString()}
}
'''
js = execjs.compile(js_code)

timestamp = int(time.time() * 1000)

x_auth_token= js.call('get_x_auth_token')


def get_captch():
    print(f"{'*'*50}正在识别验证码{'*'*50}")
    while True:
        captcha_url = f'https://www.caasbuy.com/uac/captcha.jpg?t={timestamp}'

        captcha_dict = js.call('get_sign', captcha_url)

        captcha_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "sign": captcha_dict['sign'],
            "nonce": f"{captcha_dict['nonce']}",
            "x-auth-token": f"{x_auth_token}"
        }
        captcha_resp = requests.get(url=captcha_url, headers=captcha_headers)
        captcha_resp.encoding = 'utf-8'
        with open('img.png', 'wb') as f:
            f.write(captcha_resp.content)

        image_obj = Image.open('img.png')
        img = image_obj.convert("L")

        pixdata = img.load()
        w, h = img.size
        threshold = 160
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        # img.show()
        img_byte = BytesIO()
        img.save(img_byte, format='PNG')  # format: PNG or JPEG
        binary_content = img_byte.getvalue()
        bs64_img = base64.b64encode(binary_content)
        # 获取token
        # 百度api
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=自行填充&client_secret=自行填充'
        response = requests.get(host)
        access_token = response.json()['access_token']

        bd_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token={}".format(access_token)

        data = {
            "image": bs64_img
        }

        resp = requests.post(url=url, headers=bd_headers, data=data)

        try:
            result = resp.json()['words_result'][0]['words']

        except Exception as e:
            print("识别失败:重新验证")
            result = '0'
        if len(result) == 4:
            break
    print(f"{'*'*50}验证码识别成功:{result}{'*'*50}")
    return result


def get_password(password):
    print(f"{'*'*50}正在获取aes_password{'*'*50}")
    aes_key_url = f'https://www.caasbuy.com/uac/getKey?t={timestamp}'
    aes_sign_dict = js.call('get_sign', aes_key_url)
    aes_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "sign": aes_sign_dict['sign'],
        "nonce": f"{aes_sign_dict['nonce']}",
        "x-auth-token": f"{x_auth_token}"
    }
    aes_resp = requests.get(url=aes_key_url, headers=aes_headers)

    aes_key = aes_resp.json()['data']
    aes_password = js.call("get_passwd", password, aes_key)['password']
    print(f"{'*'*50}获取aes_password成功:{aes_password}{'*'*50}")
    return aes_password


def login(captch_code, username, password):
    print(f"{'*'*50}正在登录{'*'*50}")
    login_url = f'https://www.caasbuy.com/uac/oauth/token?captcha={captch_code}'
    login_sign_dict = js.call('get_sign', login_url)
    login_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "sign": login_sign_dict['sign'],
        "nonce": f"{login_sign_dict['nonce']}",
        "Authorization": "自行抓包填充",
        "x-auth-token": f"{x_auth_token}"
    }
    data = {
        "username": username,
        "grant_type": "password",
        "scope": "all",
        "password": f"{password}",
    }
    login_resp = requests.post(url=login_url, headers=login_headers, data=data)
    access_token = login_resp.json()
    print(access_token)
    print(f"{'*'*50}登录成功{'*'*50}")
    return access_token['access_token']


def get_detail_item(url, access_token):
    res_dict = js.call('get_sign', url)
    headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "nonce": str(res_dict['nonce']),
        "sign": res_dict['sign'],
    }
    reps = requests.get(url=url, headers=headers)
    return reps.json()


if __name__ == '__main__':
    username = ''
    password = ''
    captch_code = get_captch()
    aes_password = get_password(password=password)
    access_token = login(captch_code=captch_code, username=username, password=aes_password)
    url = f'https://www.caasbuy.com/supplier/v1/order/detail/产品id?t={timestamp}'
    item_info = get_detail_item(url=url, access_token=access_token)
    print(item_info)
