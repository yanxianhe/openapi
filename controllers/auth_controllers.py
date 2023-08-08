#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   auth_controllers.py
@Time    :   2023/08/08 21:09:40
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''

from fastapi import Header, Request

async def auth_controllers_get_token(
    request: Request,
    service_addres: str = Header("https://172.16.0.17", description="https://ip:port"),
    access_key: str = Header("23977799", description="Access Key")):
    return "23977799"


# 处理函数示例
async def ping(request: Request):
    # 查询第三方依赖[影响系统运行的条件]
    # 不影响系统运行返回成功
    return {"message": request.url}