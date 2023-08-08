
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_hmac.py
@Time    :   2023/08/04 14:07:47
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''



import base64
import hmac
import hashlib


def generate_message(ak, sk, url):
    signing_key = bytes(sk, 'utf-8')
    message = "POST\n*/*\napplication/json\nx-ca-key:%s\n%s" % (ak,url)
    signature = hmac.new(signing_key, msg=bytes(message, 'utf-8'), digestmod=hashlib.sha256).digest()
    encoded_signature = base64.b64encode(signature).decode('utf-8')
    return encoded_signature



ak = "23977799"
sk = 'onihBfjbZfkgUNnsnKbD'
url = "/artemis/api/v1/oauth/token"
signature = generate_message(ak, sk,url)
print(signature)


import random
import string

def generate_transaction_code():
    characters = string.ascii_uppercase + string.digits  # 使用大写字母和数字
    transaction_code = ''.join(random.choices(characters, k=12))  # 从字符集中随机选择12个字符
    return transaction_code

# 生成交易码示例
transaction_code = generate_transaction_code()
print(transaction_code)


import hashlib
import hmac
import base64
import os,uuid


def getUuid1():
    return (str(uuid.uuid1()).replace("-", ""))

def generate_ak_sk():
    # 生成随机的 AK 和 SK
    ak = os.urandom(16).hex().upper()
    sk = os.urandom(32).hex()
    return ak, sk

def sign_request(sk, data):
    # 使用 SK 对数据进行签名
    signature = hmac.new(bytes.fromhex(sk), data.encode(), hashlib.sha256).digest()
    # 将签名进行base64编码
    signed_request = base64.b64encode(signature).decode()
    return signed_request

# 生成 AK 和 SK 示例
ak, sk = generate_ak_sk()
print("AK:", ak)
print("SK:", sk)

# 使用 SK 对数据进行签名示例
data = "example-data"
signed_request = sign_request(sk, data)
print("Signed Request:", signed_request)