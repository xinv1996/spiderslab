import base64
import json
import re
import time
import hashlib
from urllib.parse import urljoin

import execjs
import requests
def main():
    sss = """const  askH3G2f8hoq = "aJoQtX23yozrU3lC";//AESkey，可自定义
    const  asiI0QI5rULO = "bCHVjx8NioaVDasQ";//密钥偏移量IV，可自定义
    const  ackgvCsBCbUz = "dVBr2f9OdFEWJuvr";//AESkey，可自定义
    const  aciivmnCJjop = "ffxSh6rArNJMRu9c";//密钥偏移量IV，可自定义
    const  dskW8VQd4hi2 = "hfROFWOYOfqNDpLe";//DESkey，可自定义
    const  dsiQIHQX3fBz = "xmWA34EVWHFgaoZk";//密钥偏移量IV，可自定义
    const  dckeCHDjiP3k = "oWSh3LPWpfM4S9up";//DESkey，可自定义
    const  dcicbgjuN9xM = "p6ks8Spt5G8mtRFX";//密钥偏移量IV，可自定义
    const aes_local_key = 'emhlbnFpcGFsbWtleQ==';
    const aes_local_iv = 'emhlbnFpcGFsbWl2';
    var BASE64 = {
        encrypt: function(text) {
            var b = new Base64();
            return b.encode(text);
        },
        decrypt: function(text) {
            var b = new Base64();
            return b.decode(text);
        }
    };
    
    var DES = {
     encrypt: function(text, key, iv){
        var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.DES.encrypt(text, secretkey, {
          iv: secretiv,
          mode: CryptoJS.mode.CBC,
          padding: CryptoJS.pad.Pkcs7
        });
        return result.toString();
     },
     decrypt: function(text, key, iv){
        var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.DES.decrypt(text, secretkey, {
          iv: secretiv,
          mode: CryptoJS.mode.CBC,
          padding: CryptoJS.pad.Pkcs7
        });
        return result.toString(CryptoJS.enc.Utf8);
      }
    };
    
    var AES = {
      encrypt: function(text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
        // console.log('real key:', secretkey);
        // console.log('real iv:', secretiv);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.AES.encrypt(text, secretkey, {
          iv: secretiv,
          mode: CryptoJS.mode.CBC,
          padding: CryptoJS.pad.Pkcs7
        });
        return result.toString();
      },
      decrypt: function(text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.AES.decrypt(text, secretkey, {
          iv: secretiv,
          mode: CryptoJS.mode.CBC,
          padding: CryptoJS.pad.Pkcs7
        });
        return result.toString(CryptoJS.enc.Utf8);
      }
    };
    
    var localStorageUtil = {
      save: function(name, value) {
        var text = JSON.stringify(value);
        text = BASE64.encrypt(text);
        text = AES.encrypt(text, aes_local_key, aes_local_iv);
        try {
          localStorage.setItem(name, text);
        } catch (oException) {
          if (oException.name === 'QuotaExceededError') {
            console.log('Local limit exceeded');
            localStorage.clear();
            localStorage.setItem(name, text);
          }
        }
      },
      check: function(name) {
        return localStorage.getItem(name);
      },
      getValue: function(name) {
        var text = localStorage.getItem(name);
        var result = null;
        if (text) {
          text = AES.decrypt(text, aes_local_key, aes_local_iv);
          text = BASE64.decrypt(text);
          result = JSON.parse(text);
        }
        return result;
      },
      remove: function(name) {
        localStorage.removeItem(name);
      }
    };
    
    // console.log('base64', BASE64.encrypt('key'));
    
    function dOz9ddS2f9j(p3p1lY7) {
      p3p1lY7 = DES.decrypt(p3p1lY7, dskW8VQd4hi2, dsiQIHQX3fBz);
      return p3p1lY7;
    }
    
    function dlj93SrB6V(p3p1lY7) {
      p3p1lY7 = AES.decrypt(p3p1lY7, askH3G2f8hoq, asiI0QI5rULO);
      return p3p1lY7;
    }
    
    function gSdoB01Y9Tg2Fike(key, period) {
        if (typeof period === 'undefined') {
            period = 0;
        }
        var d = DES.encrypt(key);
        d = BASE64.encrypt(key);
        var data = localStorageUtil.getValue(key);
        if (data) { // 判断是否过期
            const time = data.time;
            const current = new Date().getTime();
            if (new Date().getHours() >= 0 && new Date().getHours() < 5 && period > 1) {
                period = 1;
            }
            if (current - (period * 60 * 60 * 1000) > time) { // 更新
               data = null;
            }
            // 防止1-5点用户不打开页面，跨天的情况
            if (new Date().getHours() >= 5 && new Date(time).getDate() !== new Date().getDate() && period === 24) {
               data = null;
            }
        }
        return data;
    }
    
    function osKNak2xR5(obj) {
        var newObject = {};
        Object.keys(obj).sort().map(function(key){
          newObject[key] = obj[key];
        });
        return newObject;
    }
    function dWeakEZ9h6J6(data) {
        data = BASE64.decrypt(data);
        data = DES.decrypt(data, dskW8VQd4hi2, dsiQIHQX3fBz);
        data = AES.decrypt(data, askH3G2f8hoq, asiI0QI5rULO);
        data = BASE64.decrypt(data);
        return data;
    }
    var pCvG1DPhnVpa = (function(){
    
    function osKNak2xR5(obj){
        var newObject = {};
        Object.keys(obj).sort().map(function(key){
            newObject[key] = obj[key];
        });
        return newObject;
    }
    return function(mgp9V1Jf1, oabuwM){
        var aQ5W = '5c4c8f09422523121332ea6c36f5c5dd';
        var cJZC0 = 'WEB';
        var tT0iESD = new Date().getTime();
    
        var p3p1lY7 = {
          appId: aQ5W,
          method: mgp9V1Jf1,
          timestamp: tT0iESD,
          clienttype: cJZC0,
          object: oabuwM,
          secret: hex_md5(aQ5W + mgp9V1Jf1 + tT0iESD + cJZC0 + JSON.stringify(osKNak2xR5(oabuwM)))
        };
        p3p1lY7 = BASE64.encrypt(JSON.stringify(p3p1lY7));
        p3p1lY7 = DES.encrypt(p3p1lY7, dckeCHDjiP3k, dcicbgjuN9xM);
        return p3p1lY7;
    };
    })();
    
    function s0y5uzoESwq4Y9u3xBXh(mgp9V1Jf1, o08eB72bkL, ccysruM6B, pQvrWht) {
        const kwzz = hex_md5(mgp9V1Jf1 + JSON.stringify(o08eB72bkL));
    
        const d50fq = gSdoB01Y9Tg2Fike(kwzz, pQvrWht);
        if (!d50fq) {
            var p3p1lY7 = pCvG1DPhnVpa(mgp9V1Jf1, o08eB72bkL);
            $.ajax({
                url: 'api/historyapi.php',
                data: { hEGCupyyO: p3p1lY7 },
                type: "post",
                success: function (d50fq) {
                    d50fq = dWeakEZ9h6J6(d50fq);
                    oabuwM = JSON.parse(d50fq);
                    if (oabuwM.success) {
                        if (pQvrWht > 0) {
                          oabuwM.result.time = new Date().getTime();
                          localStorageUtil.save(kwzz, oabuwM.result);
                        }
                        ccysruM6B(oabuwM.result);
                    } else {
                        console.log(oabuwM.errcode, oabuwM.errmsg);
                    }
                }
            });
        } else {
            ccysruM6B(d50fq);
        }
    }
    """

    keys = re.findall(r'DES.encrypt\((\w+)\s?,\s?(\w+)\s?,\s?(\w+)\)', sss)
    text_name, key_name, iv_name = keys[0]
    key = re.findall(f'const\s+?{key_name}\s+?=.*?"(.*?)"', sss)[0]
    iv = re.findall(f'const\s+?{iv_name}\s+?=.*?"(.*?)"', sss)[0]
    appid_name = re.findall("appId:.*?(\w+),", sss)[0]
    appId = re.findall(f"var\s?{appid_name}\s?=.*?'(.*?)'", sss)[0]

    param_name = re.findall("data:\s?\{\s?(\w+):.*?}", sss)[0]

    js_code = """ CryptoJS = require('Crypto-js')
            function des_encrypt (text, key, iv) {
            var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
            var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
            secretkey = CryptoJS.enc.Utf8.parse(secretkey);
            secretiv = CryptoJS.enc.Utf8.parse(secretiv);
            var result = CryptoJS.DES.encrypt(text, secretkey, {
                iv: secretiv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            return result.toString();
        }"""

    js = execjs.compile(js_code)

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

if __name__ == '__main__':
    url = "https://www.aqistudy.cn/historydata/daydata.php?city=%E4%B8%B4%E6%B2%82&month=2020-05"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.aqistudy.cn",
        "Referer": "https://www.aqistudy.cn/historydata/daydata.php?city=%E4%BF%9D%E5%AE%9A&month=202009",
    }
    req = requests.get(url,headers=headers)
    js_url= re.findall(r'src="(resource/js/.*?.min.js\?v=\d+)"',req.text)[0]
    js_req = requests.get(url=urljoin(url,js_url),headers=headers)
    js_bs64_bs64_code = f"a = {js_req.text}"
    res = execjs.compile(js_bs64_bs64_code)
    # print(res)

    print(js_req.text)
