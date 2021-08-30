# -*- coding:utf-8 -*-
# @project: spiderslab
# @software: GoLand

import json

import execjs
import requests
false,true,null = False,True,None
jscode = open('xiniu.js', 'r').read()
js = execjs.compile(jscode)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Cookie": "你自己的cookie！！！！！！！！！！！！！！！！！！！！！！！！！！！",
}
# 获取公司列表

list_url = 'https://www.xiniudata.com/api/search3/company/search_company_for_lib'


list_data = {"payload":{"tag_names":[],"corporate_regionIds":[1],"corporate_provinceIds":[],"corporate_cityIds":[],"corporate_districtIds":[],"corporate_establishDate_start":null,"corporate_establishDate_end":null,"funding_fundingDate_start":null,"funding_fundingDate_end":null,"corporate_locationIds":[],"corporate_rounds":[],"operator":"and","notFromGongshang":true,"sort":76006,"order":-1,"start":0,"limit":20,"domestic":null}}

list_req_data = js.call('get_request_payload', list_data)
list_req = requests.post(url=list_url, headers=headers, json=json.loads(list_req_data))
list_res_data = js.call('get_data', list_req.json()['d'])

print(list_res_data)


# 获取公司详情
# target_company = {"payload":{"codes":["jufengoulu"]}}
#
# req_data = js.call('get_request_payload', target_company)
#
# cimpany_url = 'https://www.xiniudata.com/api2/service/x_service/person_company4_list/list_companies4_list_by_codes'
#
# req = requests.post(url=cimpany_url, headers=headers, json=json.loads(req_data))
#
# res_data = js.call('get_data', req.json()['d'])
#
# print(res_data)

# {"code":0,"list":[{"id":209607,"corporateId":207846,"code":"jufengoulu","name":"维基链","fullName":null,"brief":"区块链底层平台","description":null,"logo":"https://api.xiniudata.com/file/02c0bcba5d2d11e98c2200163e03b331","round":1130,"roundName":"战略投资","roundDesc":null,"locationName":"深圳","establishDate":1496246400000,"companyStatus":"2010","statusDate":0,"website":null,"funding":{"id":343677,"round":0,"roundName":"战略投资","fundingDate":1611446400000,"fundingType":0,"publishDate":1611446400000,"source":69999,"gsDetectDate":0,"gsChangeDate":0,"corporateId":207846,"companyId":209607,"newsLink":"/news/600ed30fdeb471097836f88d","outerLink":null,"fundingDesc":"{\"postMoney\":\"未披露\",\"postBrief\":\"\",\"money\":\"1500万美元\",\"investorStr\":\"[{\\\"text\\\":\\\"AEX交易所\\\",\\\"id\\\":51682,\\\"type\\\":\\\"investor\\\"}]\",\"faBrief\":\"\",\"fa\":null,\"ratio\":null,\"roundBrief\":\"获得1500万美元战略投资，\"}","topic":null,"topicMessagePublishTime":1611556699000,"stockExchange":null,"stockExchangeBoard":null},"tagNameList":["区块链"],"regionName":"中国","provinceName":"广东省","cityName":"深圳市","districtName":"龙华区"}]}
