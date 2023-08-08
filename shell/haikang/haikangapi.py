#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   haikangapi.py
@Time    :   2023/08/04 15:55:07
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''

###*************************             FastAPI init            *****************************#######
###*******************************************************************************************#######
import os,base64,hashlib,hmac,uuid
from fastapi import Body, FastAPI, Header,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests,urllib3,json,logging
import redis


urllib3.disable_warnings()
logging.captureWarnings(True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

description = """xianhe_yan@sina.com"""
tags_metadata = [
    {
        "name": "token",
        "description": "获取海康token",
    },
    {
        "name": "root",
        "description": "获取根区域信息接口",
    },
    {
        "name": "resources",
        "description": "获取资源列表v2",
    },
    {
        "name": "search",
        "description": "查询编码设备列表v2.根据条件查询目录下有权限的编码设备列表。",
    },


]

ACCESS_KEY = os.environ.get('ACCESS_KEY', '23977799')
SECRET_KEY = os.environ.get('SECRET_KEY', 'onihBfjbZfkgUNnsnKbD')

_autn={ACCESS_KEY:SECRET_KEY}


## 交易列表
# 获取 token
_ARTEMIS_TOKEN = "/artemis/api/v1/oauth/token"
# 获取跟
_ARTEMIS_ROOT = "/artemis/api/resource/v1/regions/root"
# 获取资源列表v2
_ARTEMIS_RESOURCES = "/artemis/api/irds/v2/deviceResource/resources"
# 查询编码设备列表v2
_ARTEMIS_SEARCH = "/artemis/api/resource/v2/encodeDevice/search"

class redis_client(object) :
    
    def __init__(self) :
        # 如果环境变量不存在，返回默认值'Default Value'
        redis_host = os.environ.get('DB_HOST', '127.0.0.1')
        redis_port = os.environ.get('DB_PORT', '6379')
        redis_dbname = os.environ.get('DB_NAME', 0)
        # 创建Redis连接
        self.db0 = redis.Redis(host=redis_host, port=redis_port, db=redis_dbname)
        
## uuid
def getUuid1():
    return (str(uuid.uuid1()).replace("-", ""))
## 海康获取 x-ca-signature
def getSignature (access_key, sk, url) :
    signing_key = bytes(sk, 'utf-8')
    message = "POST\n*/*\napplication/json\nx-ca-key:%s\n%s" % (access_key,url)
    signature = hmac.new(signing_key, msg=bytes(message, 'utf-8'), digestmod=hashlib.sha256).digest()
    _xcasignature = base64.b64encode(signature).decode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8',
        'x-ca-key': access_key,
        'x-ca-signature-headers': 'x-ca-key',
        'x-ca-signature': _xcasignature
    }
    return _xcasignature,headers

def req_headers(access_token):
    
    _token = access_token.get("access_token")

    headers = {
        'access_token': _token,
        'Content-Type': 'application/json'
    }
    return _token,headers



try:
    app = FastAPI(
        title="接口转换",
        description=description,
        summary="",
        version="v0.0.1",
        openapi_tags=tags_metadata,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logging.info("[success] running  http://127.0.0.1:8000 (Press CTRL+C to quit) ")
except Exception as e:
    logging.error("[error] running  %s" % e)
    raise e


def get_token(ak):
     ## 获取存储在Redis中的JSON数据
    redis = redis_client()
    stored_json = redis.db0.get(ak)
    return stored_json
def pull_token(ak,json_data):
     ## 存储在Redis中的JSON数据
    redis = redis_client()
    redis.db0.setex(ak, 11 * 60 * 60, json_data)
    redis.db0.close()
    return json_data


def send_http(_uuid,_requrl,_headers,payload = {}):
   
    try:
        response = requests.request("POST", _requrl, headers=_headers, data=payload,verify=False,timeout=10)
        data = (json.loads(response.text))
        if data["msg"] == "success" :
            _dict_data = data["data"]
            _dict_data['code']=data["code"]
            _dict_data['message']=data["msg"]
        else:
            _dict_data == data
           
    except requests.exceptions.Timeout :
        msg = ("[%s] Internal Server TimeoutException" % _requrl)
        logging.error(("[%s] {%s}" % (_uuid, msg)))
        return msg
    except requests.exceptions.ConnectionError as e:
        msg = ("[%s] Internal Server Exception" % _requrl)
        logging.error(("[%s] {%s}" % (_uuid, msg)))
        return "Internal Server Exception %s" % e
    except requests.exceptions.HTTPError as e :
        logging.error(("[%s] {%s}" % (_uuid, msg)))
        return "Internal Server Exception 0 %s" % e
    return _dict_data
    

@app.get("/v1/token",tags=["token"])
async def read_token(
    request: Request,
    service_addres: str = Header("https://172.16.0.17", description="https://ip:port"),
    access_key: str = Header("23977799", description="Access Key")):
    
    secret_key = _autn.get(access_key)
    if not secret_key:
        return "msg:无此账号 %s" % access_key
    
    _uuid = getUuid1()
    _requrl = ("%s%s")%(service_addres,_ARTEMIS_TOKEN)
    logging.info(("[%s][%s] {%s} " % (_uuid,request.client.host ,_requrl)))
     ## 获取存储在Redis中的JSON数据
    _token_json = get_token(access_key)
    if _token_json is not None:
        access_token = json.loads(_token_json)
        logging.info(("[%s] {%s}" % (_uuid, access_token)))
        return access_token
    ## 通过接口获取
    _xcasignature,_headers = getSignature(access_key,secret_key,_ARTEMIS_TOKEN);
    access_token = send_http(_uuid,_requrl,_headers)
    # 设置键-值对，将JSON存储到Redis中，并设置过期时间为11小时
    pull_token(access_key,json.dumps(access_token))
    logging.info(("[%s] {%s}" % (_uuid, access_token)))

    return access_token

@app.post("/v1/root",tags=["root"])
async def read_root(
    request: Request,
    service_addres: str = Header("https://172.16.0.17", description="https://ip:port"),
    access_key: str = Header("23977799", description="Access Key"),
    treeCode: str = "0"):
    
    secret_key = _autn.get(access_key)
    if not secret_key:
        return "msg:无此账号 %s" % access_key
    
    _uuid = getUuid1()
    _requrl = ("%s%s")%(service_addres,_ARTEMIS_ROOT)
    logging.info(("[%s][%s] {%s} " % (_uuid,request.client.host ,_requrl)))
    
     ## 获取存储在Redis中的JSON数据
    _token_json = get_token(access_key)
    if _token_json is not None:
        access_token = json.loads(_token_json)
        
    else : 
        ## 通过接口获取
        _tokenurl = ("%s%s")%(service_addres,_ARTEMIS_TOKEN)
        secret_key = _autn.get(access_key)
        _xcasignature,_headers = getSignature(access_key,secret_key,_ARTEMIS_TOKEN);
        access_token = send_http(_uuid,_tokenurl,_headers)
        # 设置键-值对，将JSON存储到Redis中，并设置过期时间为11小时
        pull_token(access_key,json.dumps(access_token))
    
    payload = json.dumps({
        "treeCode": treeCode
    })
    
    _token,_headers = req_headers(access_token)
    _root_data = send_http(_requrl,_headers,payload)
    logging.info(("[%s] {%s} {%s}" % (_uuid, _requrl,payload)))
    return _root_data




@app.post("/v1/deviceResource/resources",tags=["resources"])
async def read_resources(
    request: Request,
    service_addres: str = Header("https://172.16.0.17", description="https://ip:port"),
    access_key: str = Header("23977799", description="Access Key"),
    pageNo: int = Body(1,embedy=True), 
    pageSize: int = Body(100,embedy=True), 
    resourceType: str =  Body("camera",embedy=True),
    orderBy: str = Body("createTime",embedy=True),
    orderType: str = Body("asc",embedy=True)):
    
    secret_key = _autn.get(access_key)
    if not secret_key:
        return "msg:无此账号 %s" % access_key
    
    _uuid = getUuid1()
    _requrl = ("%s%s")%(service_addres,_ARTEMIS_RESOURCES)
    logging.info(("[%s][%s] {%s} " % (_uuid,request.client.host ,_requrl)))
    
     ## 获取存储在Redis中的JSON数据
    _token_json = get_token(access_key)
    if _token_json is not None:
        access_token = json.loads(_token_json)
        
    else : 
        ## 通过接口获取
        _tokenurl = ("%s%s")%(service_addres,_ARTEMIS_TOKEN)
        secret_key = _autn.get(access_key)
        _xcasignature,_headers = getSignature(access_key,secret_key,_ARTEMIS_TOKEN);
        access_token = send_http(_tokenurl,_headers)
        # 设置键-值对，将JSON存储到Redis中，并设置过期时间为11小时
        pull_token(access_key,json.dumps(access_token))
    
    
    payload = json.dumps({
    "pageNo": pageNo,
    "pageSize": pageSize,
    "resourceType": resourceType,
    "orderBy": orderBy,
    "orderType": orderType
    })
        
    _token,_headers = req_headers(access_token)
    _root_data = send_http(_uuid,_requrl,_headers,payload)
    logging.info(("[%s] {%s} {%s}" % (_uuid, _requrl,payload)))
    
    return _root_data


@app.post("/v1/encodeDevice/search",tags=["search"])
async def read_search(
    request: Request,
    service_addres: str = Header("https://172.16.0.17", description="https://ip:port"),
    access_key: str = Header("23977799", description="Access Key"),
    pageNo: int = Body(1,embedy=True), 
    pageSize: int = Body(100,embedy=True), 
    regionIndexCodes: list =  Body([],embedy=True),
    orderBy: str = Body("createTime",embedy=True),
    orderType: str = Body("asc",embedy=True)):
    
    secret_key = _autn.get(access_key)
    if not secret_key:
        return "msg:无此账号 %s" % access_key
    
    _uuid = getUuid1()
    _requrl = ("%s%s")%(service_addres,_ARTEMIS_SEARCH)
    logging.info(("[%s][%s] {%s} " % (_uuid,request.client.host ,_requrl)))
    
     ## 获取存储在Redis中的JSON数据
    _token_json = get_token(access_key)
    if _token_json is not None:
        access_token = json.loads(_token_json)
        
    else : 
        ## 通过接口获取
        _tokenurl = ("%s%s")%(service_addres,_ARTEMIS_TOKEN)
        secret_key = _autn.get(access_key)
        _xcasignature,_headers = getSignature(access_key,secret_key,_ARTEMIS_TOKEN);
        access_token = send_http(_tokenurl,_headers)
        # 设置键-值对，将JSON存储到Redis中，并设置过期时间为11小时
        pull_token(access_key,json.dumps(access_token))
    

    
    payload = json.dumps({
    "regionIndexCodes":regionIndexCodes,
    "pageNo": pageNo,
    "pageSize": pageSize,
    "orderBy": orderBy,
    "orderType": orderType
    })

        
    _token,_headers = req_headers(access_token)
    _root_data = send_http(_uuid,_requrl,_headers,payload)
    logging.info(("[%s] {%s} {%s}" % (_uuid, _requrl,payload)))
    
    return _root_data