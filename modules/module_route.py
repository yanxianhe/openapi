#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   module_route.py
@Time    :   2023/08/07 23:36:27
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''



import pymysql
from sqlalchemy import TIMESTAMP, Column, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modules.db_client import MySQLAlchemyClient
from loguru import logger
from public.sys_logs import GetLogging


# 引入日志
GetLogging().get()
# 以便与 SQLAlchemy 兼容 ORM
pymysql.install_as_MySQLdb()


# 声明基类
Base = declarative_base()


class Route(Base):
    __tablename__ = "interfaces"
    __table_args__ = {"comment": "主路由接口表."}
    transaction_id = Column(String(32), primary_key=True, comment="接口交易码id")
    name = Column(String(254), nullable=False, comment="接口名")
    path = Column(String(254), nullable=False, comment="接口路径")
    method = Column(String(16), nullable=False, comment="请求方式")
    controller = Column(String(254),nullable=False,server_default="hello_world",comment="接口controller入口",)
    system_id = Column(String(16), nullable=False, comment="系统id")
    tags = Column(String(64), nullable=False, comment="接口tags描述在metadata维护")
    transaction_status = Column(String(16), nullable=False, server_default="00", comment="接口状态 00:正常 01:测试接口 02:停止对外服务")
    description = Column(String(254), nullable=False, comment="接口描述信息")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    def __init__(self,transaction_id,name,path,method,controller,system_id,tags,transaction_status,description,created_at):
        self.transaction_id = transaction_id
        self.name = name
        self.path = path
        self.method = method
        self.controller = controller
        self.system_id = system_id
        self.tags = tags
        self.transaction_status = transaction_status
        self.description = description
        self.created_at = created_at


    ## toString
    def __str__(self):
        _interfaces = f"(transaction_id={self.transaction_id},name={self.name},path={self.path},method={self.method},controller={self.controller},system_id={self.system_id},tags={self.tags},transaction_status={self.transaction_status},description={self.description},created_at={self.created_at})"
        return _interfaces


    def query():
        _results = ""
        _myquery = MySQLAlchemyClient()
        _MySession = sessionmaker(bind=_myquery.engine)
        try:
            _session = _MySession()
            _results = _session.query(Route).all()
            pass
        except Exception as e:
            logger.error("Route.query  error ,%s " % e)
            return e
        finally :
            _session.close()
        return _results
    
## 创建会话
_my = MySQLAlchemyClient()
Session = sessionmaker(bind=_my.engine)
## 创建表如果存在 ，则忽略
Base.metadata.create_all(_my.engine)

# session = Session()
# # 分页查询
# page_size = 20  # 每页的记录数
# page_number = 1  # 页码，从1开始

# # 计算偏移量
# offset = (page_number - 1) * page_size
# # 查询数据并进行分页
# results = session.query(Route).offset(offset).limit(page_size).all()


# json_list = []
# # 遍历结果
# for result in results:
#     # 处理每条记录
#     json_list.append(result)
#     print("%s"%result)
    

