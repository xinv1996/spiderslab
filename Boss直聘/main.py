import random
from urllib import parse
from urllib.parse import quote

import execjs
import requests

from ua_pool import chrome

if __name__ == '__main__':
    ua = random.choice(chrome)
    sess = requests.Session()
    proxies = {'http': 'http://127.0.0.1:1086', 'https': 'https://127.0.0.1:1086'}
    headers = {
        "user-agent": f"ua",
    }
    url = "https://www.zhipin.com/job_detail/?query=%E5%8C%97%E4%BA%AC%E4%B9%BE%E5%9D%A4%E9%95%BF%E5%8D%BF%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"
    response = requests.get(url, headers=headers, proxies=proxies)
    query_str = parse.urlparse(response.url).query
    query_dict = {i.split("=")[0]: i.split("=")[1] for i in query_str.split("&")}
    seed = parse.unquote(query_dict.get("seed"))
    ts = query_dict.get("ts")
    js_name = query_dict.get("name")
    js_url = f"https://www.zhipin.com/web/common/security-js/{js_name}.js"
    js_res = sess.get(js_url, headers=headers, proxies=proxies)
    js_text = js_res.text
    js_text = js_text.replace("atob", "window.atob")
    js_code_format = '''
const jsdom = require("jsdom");
const {JSDOM} = jsdom;
const dom = new JSDOM(``, {
    url: "https://www.zhipin.com/",
    cookieEnabled: true,
    language: "zh-CN",
    userAgent: "{{uablock}}",
});
window = dom.window;
var document = dom.window.document;
window.document = document;
top = window.top = window

{{contentblock}}

function get_stoken(seed, ts) {
var code = new ABC().z(seed, parseInt(ts) + 1e3 * 60 * (480 + (new Date).getTimezoneOffset()))
return encodeURIComponent(code)
}
    '''

    js_code = js_code_format.replace('{{contentblock}}', js_text).replace('{{uablock}}', ua)

    js = execjs.compile(js_code)

    zp_stoken = js.call('get_stoken', seed, ts)
    print(zp_stoken)
    headers = {
        "user-agent": f"{ua}",
        "cookie": f'__zp_stoken__={zp_stoken};__zp_sname__={js_name}; __zp_sts__={ts};__zp_sseed__={seed};',
        "referer": f"https://www.zhipin.com/web/common/security-check.html?seed={quote(seed)}&name={js_name}&ts={ts}&callbackUrl={quote(url.replace('https://www.zhipin.com', ''))}&srcReferer=",
    }
    resp = sess.get(url=url, headers=headers,
                        proxies=proxies)
    resp.encoding = 'utf-8'
    print(resp.text)

    print(resp.status_code)
