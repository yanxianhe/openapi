#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   db_client.py
@Time    :   2023/08/07 08:57:35
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''



import os
import pymysql
from loguru import logger
from redis import Redis
from redis import Redis
from sqlalchemy import create_engine

from public.sys_logs import GetLogging
from public.utils import UtilsTools

# 引入日志
GetLogging().get()
# 以便与 SQLAlchemy 兼容 ORM
pymysql.install_as_MySQLdb()

'''
数据操作 DB The starting point
'''

#########################################Python的数据操作 Redis#########################################

## 创建Redis连接
class MyredisClient(object) :
    def __init__(self) :
        # 如果环境变量不存在，返回默认值'Default Value'
        redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
        redis_port = os.environ.get('REDIS_PORT', '6379')
        redis_dbname = os.environ.get('REDIS_NAME', 0)
        # 创建Redis连接
        self.db0 = Redis.Redis(host=redis_host, port=redis_port, db=redis_dbname)

#########################################Python的数据操作 Redis#########################################

#########################################Python的数据操作 SQLAlchemy 工具和类#############################
## 使用 SQLAlchemy 工具和类 ORM 允许你通过使用对象来操作数据库，而无需直接编写 SQL 查询语句
class MySQLAlchemyClient(object):
    def __init__(self):
        # 如果环境变量不存在，返回默认值'Default Value'
        dbms = os.environ.get("DBMS", "mysql")
        db_host = os.environ.get("DB_HOST", "152.136.152.16")
        db_port = os.environ.get("DB_PORT", "63306")
        db_username = os.environ.get("DB_USER", "root")
        db_passwords = os.environ.get("DB_PASS", "root")
        db_dbname = os.environ.get("DB_NAME", "test")
        sql = ("%s://%s:%s@%s:%s/%s") % (dbms,db_username,db_passwords,db_host,db_port,db_dbname)
        self.engine = create_engine(sql)

#########################################Python的数据操作 SQLAlchemy 工具和类#############################


#########################################Python的数据操作 原生mysql#########################################
class MysqlClient (object) :
    def __init__(self) :
        # 如果环境变量不存在，返回默认值'Default Value'
        mysql_host = os.environ.get('MYSQL_HOST', '152.136.152.16')
        mysql_port = os.environ.get('MYSQL_PORT', '63306')
        mysql_username = os.environ.get('MYSQL_USER', 'root')
        mysql_passwords = os.environ.get('MYSQL_PASS', 'root')
        mysql_dbname = os.environ.get('MYSQL_NAME', 'default')
        # 标识号
        self.Serialid = UtilsTools().getUuid1()
        
        # 打开数据库连接
        self.db = pymysql.connect(host=mysql_host,port=mysql_port,user=mysql_username,password=mysql_passwords,db=mysql_dbname,charset='utf8')
    # 查询数据返回 list 结果
    def queryList(self,temp_sql) :
        logger.info("{%s}:: query SQL:\t{%s} " % (self.Serialid,temp_sql))
        try:
            # 使用cursor()方法获取操作游标 
            cur = self.db.cursor()
            cur.execute(temp_sql)
            result = cur.fetchall()
            logger.info("{%s}:: results:\t{%s}" % (self.Serialid,result))
            return (result)
        except Exception as e :
            logger.info("querylist error ,%s " % e)
            return e
        finally:
            # 关闭指针对象
            cur.close()
            # 关闭数据库连接对象
            self.db.close()
    # 查询数据库返回 COUNT(*)
    def queryNumber(self,temp_sql) :
        logger.info("{%s}:: query SQL:\t{%s} " % (self.Serialid,temp_sql))
        try:
            # 使用cursor()方法获取操作游标 
            cur = self.db.cursor()
            cur.execute(temp_sql)
            result = [tuple[0] for tuple in cur.fetchall()]
            logger.info("{%s}:: results SQL\t{%s}" % (self.Serialid,result))
            return (result)
        except Exception as e :
            logger.info("querynumber error ,%s " % e)
            return e
        finally:
            # 关闭指针对象
            cur.close()
            # 关闭数据库连接对象
            self.db.close()
    # 更新数据返回 true/false
    def update_tables(self,temp_sql) :
        try:
            logger.info("{%s}:: update SQL:\t{%s} " % (self.Serialid,temp_sql))
            # 使用cursor()方法获取操作游标 
            cur = self.db.cursor()
            cur.execute(temp_sql)
            self.db0.commit()
            logger.info("{%s}:: results:\t{%s}" % (self.Serialid,True))
            return True
        except Exception as e :
            cur.rollback()
            logger.info("querynumber error ,%s " % e)
            return False
        finally:
            # 关闭指针对象
            cur.close()
            # 关闭数据库连接对象
            self.db.close()
#########################################Python的数据操作 原生mysql#########################################






## 查询配置表;在此表中status 状态 '1'的数据都同步
def query_sync_table() :
    _MysqlClient = MysqlClient()
    sql = "SELECT `id`, `databases`, `tables`, `starttime`, `initrows`, `rowsnumber`, `number`, `serviceip`,`serviceport`,`status` FROM `counts`.`syncrecord`  WHERE `status` = 1 LIMIT 0, 5000;"
    query_sync_table_lists = _MysqlClient.queryList(sql)
    return(query_sync_table_lists)
## 更新标准数据
def update_standard_data(number,databases,tables) :
    _MysqlClient = MysqlClient()
    sql_update = " UPDATE `counts`.`syncrecord` SET  `rowsnumber` = %s WHERE `databases` = '%s' AND `tables` = '%s'; " % (number,databases,tables)
    flg = _MysqlClient.update_tables(sql_update)
    return flg


## 更新ip数据
def update_sendserverinfo(ip,port,databases,tables) :
    _MysqlClient = MysqlClient()
    if ip != None and port != None:
        sql_update = "UPDATE counts.syncrecord SET serviceip = '%s' , serviceport = '%s' WHERE 1 = 1 ; " % (ip,port)
    else: 
        sql_update = "UPDATE counts.syncrecord SET serviceip = '%s' , serviceport = '%s' WHERE `databases` = '%s' AND `tables` = '%s'; " % (ip,port,databases,tables)  
    flg = _MysqlClient.update_tables(sql_update)
    return flg

