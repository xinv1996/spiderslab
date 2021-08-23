# -*- coding:utf-8 -*-
# @project: spiderslab
# @file: main.py
# @software: GoLand

import execjs
import requests


def bdb_func(chufa_city: str, chufa_qu: str, mudi_city: str, mudi_qu: str):
    jscode = open('bdb.js', 'r').read()
    js = execjs.compile(jscode)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }

    base_url = 'http://m.bj.bendibao.com/news/gelizhengce/gl_V5.php'

    req_k = requests.post(url=base_url, headers=headers, data={"a": "k"})

    k = req_k.json()['k']

    s = js.call('get_s', k[:-10])
    print(s)
    page = 1
    print(k)
    url = f'http://m.bj.bendibao.com/news/gelizhengce/gl_V5.php?back=1&chufa_city={chufa_city}&mudi_city={mudi_city}&chufa_qu={chufa_qu}&mudi_qu={mudi_qu}&page={page}'
    data = {
        "s": f"{k}{s}"
    }
    req = requests.post(url=url, headers=headers, data=data)

    res_data = req.json()
    print(res_data)


if __name__ == '__main__':
    chufa_city = '北京'
    mudi_city = '济南'
    chufa_qu = '大兴区'
    mudi_qu = '历下区'
    bdb_func(chufa_city, chufa_qu, mudi_city, mudi_qu)
