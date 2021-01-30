# -*- coding:utf-8 -*-
# @project: spiderslab
# @software: GoLand
import json

import execjs
import requests
import json

jscode = open('xiniu.js', 'r').read()
js = execjs.compile(jscode)

url = 'http://www.xiniudata.com/api2/service/x_service/person_company4_list/list_companies4_list_by_codes'

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Cookie": "自己的cookie"
}
# 公司代码
target_company = {"codes":["jufengoulu"]}

req_data = js.call('get_request_payload', target_company)

req = requests.post(url=url, headers=headers, json=json.loads(req_data))

res_data = js.call('get_data', req.json()['d'])

print(res_data)

# {"code":0,"list":[{"id":209607,"corporateId":207846,"code":"jufengoulu","name":"维基链","fullName":null,"brief":"区块链底层平台","description":null,"logo":"https://api.xiniudata.com/file/02c0bcba5d2d11e98c2200163e03b331","round":1130,"roundName":"战略投资","roundDesc":null,"locationName":"深圳","establishDate":1496246400000,"companyStatus":"2010","statusDate":0,"website":null,"funding":{"id":343677,"round":0,"roundName":"战略投资","fundingDate":1611446400000,"fundingType":0,"publishDate":1611446400000,"source":69999,"gsDetectDate":0,"gsChangeDate":0,"corporateId":207846,"companyId":209607,"newsLink":"/news/600ed30fdeb471097836f88d","outerLink":null,"fundingDesc":"{\"postMoney\":\"未披露\",\"postBrief\":\"\",\"money\":\"1500万美元\",\"investorStr\":\"[{\\\"text\\\":\\\"AEX交易所\\\",\\\"id\\\":51682,\\\"type\\\":\\\"investor\\\"}]\",\"faBrief\":\"\",\"fa\":null,\"ratio\":null,\"roundBrief\":\"获得1500万美元战略投资，\"}","topic":null,"topicMessagePublishTime":1611556699000,"stockExchange":null,"stockExchangeBoard":null},"tagNameList":["区块链"],"regionName":"中国","provinceName":"广东省","cityName":"深圳市","districtName":"龙华区"}]}