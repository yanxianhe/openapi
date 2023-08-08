#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2023/08/08 14:36:26
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''


import requests
import json

url = "https://172.16.0.17/artemis/api/resource/v1/regions/root"


payload = json.dumps({
  "treeCode": 0
})
headers = {
  'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJzY29wZSJdLCJleHAiOjE2OTE1MDA1MTcsImp0aSI6ImFHcml5MlBFd0RpUE1FeGVtMUtPM2w5WkhDRSIsImNsaWVudF9pZCI6IjIzOTc3Nzk5In0.-CJLg-eSaazBJRoqOxoh3Wn0fdf3Fb5I9Ib3zMcJ100',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload,verify=False,timeout=15)
data = (json.loads(response.text))
print(data)
