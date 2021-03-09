from urllib import parse
from urllib.parse import quote

import execjs
import requests


if __name__ == '__main__':
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
    sess = requests.Session()
    proxies = {'http': 'http://127.0.0.1:1086', 'https': 'https://127.0.0.1:1086'}
    headers = {
        "user-agent": f"{ua}",
    }
    url = f"https://www.zhipin.com/job_detail/?query={quote('百度')}&city=100010000&industry=&position="

    response = sess.get(url=url, headers=headers)
    query_str = parse.urlparse(response.url).query
    query_dict = {i.split("=")[0]: i.split("=")[1] for i in query_str.split("&")}
    seed = parse.unquote(query_dict.get("seed"))
    ts = query_dict.get("ts")
    js_name = query_dict.get("name")
    js_url = f"https://www.zhipin.com/web/common/security-js/{js_name}.js"
    js_res = sess.get(js_url,proxies=proxies)
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

    srcReferer = f"&srcReferer=https://www.zhipin.com/web/common/security-check.html?seed={quote(seed)}&name={js_name}&ts={ts}&callbackUrl={quote(url.replace('https://www.zhipin.com', ''))}&srcReferer="
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "user-agent": f"{ua}",
        "cookie": f'__zp_stoken__={zp_stoken}',
        "referer": f"https://www.zhipin.com/web/common/security-check.html?seed={quote(seed)}&name={js_name}&ts={ts}&callbackUrl={quote(url.replace('https://www.zhipin.com', ''))}&srcReferer=",
    }
    print(url)
    resp = sess.get(url=url, headers=headers)

    resp.encoding = 'utf-8'

    print(resp.text)
