# -*- coding:utf-8 -*-
# @file: main.py
# @desc:
import os
import json

encrypt_data = '''7W/SG3/YADnjes58i40SDb3FdL59AJp03JgJ5EpuLWagw0VNsjCDyBvROwtvNlcQ5CAZ9AoItLJTIGgoH9LhVHOHrlHdHJIYJrtPSv69Drvzumop8eYIWMaULT2h49lXXo4dxsdg1DBubhYbhRdO8fpXtJpmazGI'''

res_data = os.popen(f'node qmkj.js {encrypt_data}').read()

print(json.loads(res_data))

