# -*- coding:utf-8 -*-
# @author: xrx
# @time: 2024/3/19 12:53
# @project: SH4NH4I
# @file: main.py
# @software: PyCharm
# desc:
import cloudscraper

scraper = cloudscraper.create_scraper(delay=5, browser={
    'browser': 'chrome',
    'platform': 'linux',
    'mobile': False,

})
resp = scraper.get('https://webcache.googleusercontent.com/search?q=cache:https://www.truepeoplesearch.com/find/i',
                   proxies={'http': 'http://127.0.0.1:1996', 'https': 'http://127.0.0.1:1996'})
print(resp.text)
print(resp.status_code)
