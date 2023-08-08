#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   system.py
@Time    :   2023/08/03 00:20:45
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''

# openssl rand -hex 32

class Configs :
    SRT_KEY = '8&z9v0u5l4vkjvtx&h8&z9v0u5l4vkjvtx&8&z9v0u5l4vkjvtx&e+xt+ehmk6h)w)e-47+$tsli5g!@#$%^&*()+' 
    SECRET_KEY = "948440a0cf7c6dfd2ceeb56f9e7571201f2c6834d301ebb9c441ca267765331b"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 120



class Test:
    fake_users_db = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            # secret
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
        }
    }
