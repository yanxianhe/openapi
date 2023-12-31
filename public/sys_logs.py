#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sys_logs.py
@Time    :   2023/08/07 08:58:06
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''



import os
import datetime
from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'Default')

class GetLogging:
    """
    日志配置 根据自己情况设置
    """
 
    def __init__(self):
        # 标识号
     
        if LOG_LEVEL == "error":
            # error
            logger.add(
                os.path.join(BASE_DIR, "logs/"+"error_"+"{time:YYYY-MM-DD}.log"),
                format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                filter=lambda x: True if x["level"].name == "ERROR" else False,
                rotation="00:00", retention=7, level='ERROR', encoding='utf-8'
            )
        elif LOG_LEVEL == "info":
            # info
            logger.add(
                os.path.join(BASE_DIR, "logs/"+"info_"+"{time:YYYY-MM-DD}.log"),
                format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                filter=lambda x: True if x["level"].name == "INFO" else False,
                rotation="00:00", retention=7, level='INFO', encoding='utf-8'
            )
        elif LOG_LEVEL == "success":
            # success
            logger.add(
                os.path.join(BASE_DIR, "logs/"+"success_"+"{time:YYYY-MM-DD}.log"),
                format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                filter=lambda x: True if x["level"].name == "SUCCESS" else False,
                rotation="00:00", retention=7, level='SUCCESS', encoding='utf-8',
            )
        else:    
            # Default
            logger.add(
                os.path.join(BASE_DIR, "logs/"+"syslogs_"+"{time:YYYY-MM-DD}.log"),
                format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                rotation="00:00", retention=7, level='DEBUG', encoding='utf-8'
            )
        self.logger = logger
 
    def get(self):
        return self.logger


# globalLog = GetLogging().get()
# logger.debug("[debug] 测试 debug 级别,记录 [debug] [info] [success] [error] 级别日志")
# logger.info("[info] 测试级别日志")
# logger.success("[success] 测试级别日志")
# logger.error("[error] 测试级别日志")