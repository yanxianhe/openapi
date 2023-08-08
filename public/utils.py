
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2023/08/09 00:24:42
@Author  :   yxh 
@Version :   1.0
@Contact :   xianhe_yan@sina.com
'''





import os,uuid,base64,hashlib,hmac,random,string

from Cryptodome.Cipher import AES
from Cryptodome.Cipher import DES
from public.system import Configs

# 盐值 下面使用使用方式截取。可以直接指定
srt_key = Configs.SECRET_KEY
#srt_key = "948440a0cf7c6dfd2ceeb56f9e7571201f2c6834d301ebb9c441ca267765331b"
class UtilsTools(object) :
    
    def getUuid1(self):
        return (str(uuid.uuid1()).replace("-", ""))
    def generate_ak_sk():
        # 生成随机的 AK 和 SK
        ak = os.urandom(16).hex().upper()
        sk = os.urandom(32).hex()
        return ak, sk


#### hexdec begin

base_a = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('a'),ord('a')+6)]
base_A = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('a'),ord('a')+6)]

class hexdec(object) :
    # 反转list
    def yreverse(list):
        return list[: :-1]
    # 十六进制转十进制两位空格
    def hexlist2dec(hexlist):
        list = hexlist.split()
        l = []
        for i in list :
            l.append(int(i,16))
        return l
    # 十六进制转十进制两位空格
    def hex2dec(hexsrt):
        hex = hexsrt.replace(' ', '')
        return (int(hex,16))

    # 十进制转十六进制两位空格
    def dec2hex(num):
        i = 1
        l = []
        if num < 0:
            return '-' + hexdec.dec2hex(abs(num))
        while True:
            num,rem = divmod(num, 16)
            l.append(base_a[rem])
            if i % 2 == 0 :
                l.append(" ")
            ｉ = i + 1
            if num == 0:
                list1 = hexdec.yreverse(l)
                del list1[0]
                return ''.join(list1)
            
#### hexdec end


#### base64_tools begin


class base64_tools(object) :
    ###### base64  ######
    def srt_base64(srt_obj) :
        ## 字符串转 base64
        bs = base64.b64encode(srt_obj.encode("UTF-8"))
        # bytes 转 字符串
        return str(bs,encoding="UTF-8")
    def base64_srt(srt_obj) :
        # 字符串 转 bytes
        srt_bs = bytes(srt_obj,encoding="UTF-8")
        # base64 还原
        return base64.b64decode(srt_bs).decode("utf-8")
    def get_base64(srt_obj) :
        return  bytes(srt_obj,encoding="UTF-8")
    def get_srt(bytes_obj) :
        return  str(bytes_obj,encoding="UTF-8")
    ###### base64 end  ######
#### base64_tools end

#### pycryptos begin
class pycryptos(object) :
    #### DES #### 
    # 使用 DES加密数据的长度须为8的的倍数
    def des_encrypt(srt) :
        srt = base64_tools.srt_base64(srt)
        keys = hashlib.md5(srt_key.encode(encoding='UTF_8')).hexdigest()[0:8]
        key = bytes(keys, encoding="utf8")
        if len(srt) % 8 != 0:
            srt = srt + " " * (8 - len(srt) % 8)
        des = DES.new(key, DES.MODE_ECB)
        pas_enc = des.encrypt(srt.encode()).hex()
        return pas_enc

    def des_decrypt(pas_en) :
        
        keys = hashlib.md5(srt_key.encode(encoding='UTF_8')).hexdigest()[0:8]
        key = bytes(keys, encoding="utf8")

        des = DES.new(key, DES.MODE_ECB)
        pas_dec = des.decrypt(bytes.fromhex(pas_en))

        dtr_dec = str(pas_dec, encoding='utf-8').replace(" ","")
        return base64_tools.base64_srt(dtr_dec)
    #### DES end #### 

    #### AES ####
    def aes_encrypt(srt) :
        srt = base64_tools.srt_base64(srt)
        keys = hashlib.md5(srt_key.encode(encoding='UTF_8')).hexdigest()[0:16]
        key = bytes(keys, encoding="utf8")
        aes =  AES.new(key,AES.MODE_CFB,key)
        return aes.encrypt(srt.encode()).hex()
    def aes_decrypt(pas_en) :
        keys = hashlib.md5(srt_key.encode(encoding='UTF_8')).hexdigest()[0:16]
        key = bytes(keys, encoding="utf8")
        aes = AES.new(key, AES.MODE_CFB, key)
        pas_en = aes.decrypt(bytes.fromhex(pas_en))
        dtr_dec = str(pas_en, encoding='utf-8')
        return base64_tools.base64_srt(dtr_dec)
    #### pycryptos end




#### HmacSHA256 begin
# HmacSHA256
class hmacsha_toos(object) :
    def __init__(self) :
        
        pass
    
    # message 自定义规则
    # http_method = "POST"
    # accept = "*/*"
    # content_type = "application/json"
    # x_ca_key = "your_x_ca_key"
    #'x-ca-Signature-Headers' => 'x_ca-Key,x_ca-Nonce,x_ca-Signature-Method,x_ca-Timestamp',
    # message = f"{http_method}\n{accept}\n{content_type}\n{x_ca_key}\n{x-ca-Nonce}\n{x-ca-timestamp}\n{x-ca-Signature-Headers}"
    ## 签名
    def hmacsha_signature(ak, sk, message):
        secret = sk.encode('utf-8')
        message = ("%s%s")%(message,ak)
        signature = hmac.new(secret, message.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature
    ## 验证签名
    def verify_signature(ak, sk, message, signature):
        _hmacsha_toos= hmacsha_toos()
        generated_signature = _hmacsha_toos.hmacsha_signature(ak, sk, message)
        return signature == generated_signature
    
    def generate_signature(ak, sk):
        signing_key = bytes(ak, 'utf-8')
        signature = hmac.new(signing_key, msg=bytes(sk, 'utf-8'), digestmod=hashlib.sha256).digest()
        encoded_signature = base64.b64encode(signature).decode('utf-8')
        return encoded_signature
    
    ## 海康获取 x-ca-signature 返回headers
    def xcasignature(ak, sk, url):
        signing_key = bytes(sk, 'utf-8')
        message = "POST\n*/*\napplication/json\nx-ca-key:%s\n%s" % (ak,url)
        signature = hmac.new(signing_key, msg=bytes(message, 'utf-8'), digestmod=hashlib.sha256).digest()
        encoded_signature = base64.b64encode(signature).decode('utf-8')
        
        headers = {
            'Content-Type': 'application/json',
            'charset': 'UTF-8',
            'x-ca-key': ak,
            'x-ca-signature-headers': 'x-ca-key',
            'x-ca-signature': encoded_signature
            }
        return headers

#### HmacSHA256 end


if __name__ == "__main__":
    print(UtilsTools().getUuid1())
    
      
    # srt = "yanxa  9"
    # num = 3832426215
    # print(f"源 :: {srt} ")
    # print(f"源 :: {num} ")

    # # 字符串转 base64
    # bs = base64.b64encode(srt.encode("UTF-8"))
    # # bytes 转 字符串
    # str_obj = str(bs,encoding="UTF-8")

    # # 字符串 转 bytes
    # srt_bs = bytes(str_obj,encoding="UTF-8")
    # print(f"字符串 转 bytes::[{srt_bs}]")
    # # base64 还原
    # obj = base64.b64decode(srt_bs).decode("utf-8")
    # print(f"base64还原::[{obj}]")

    # # des 
    # enp = pycryptos.des_encrypt(srt)
    # print(f"des加密::[{enp}]")
    # pas = pycryptos.des_decrypt(enp)
    # print(f"des解密::[{pas}]")

    # # aes
    # anp = pycryptos.aes_encrypt(srt)
    # print(f"aes加密::[{anp}]")
    # pas = pycryptos.aes_decrypt(anp)
    # print(f"aes解密::[{pas}]")

    # print(f"(dec)               :: [{num}]")  
    # print(f"hex(dec)            :: [{hexdec.dec2hex(num)}]")
    # print(f"reversed hex        :: [{hexdec.dec2hex(num)[: :-1] }]") 
    # print(f"reversed hex(dec)   :: [{hexdec.hex2dec(hexdec.dec2hex(num)[: :-1])}]")
    # # 十六转十
    hex = '0x1 0x46 0x0 0x0 0x0 0x28 0x50 0x38 0x6d 0x24 0x90 0x0 0x1 0x0 0x0 0x0 0xe0 0x1 0x14 0x0 0x1f 0x0 0x23 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x9 0x5a 0xab 0x3 0xf 0xbb 0x90 0x5d 0x68'
    print(hexdec.hexlist2dec(hex))     

    
    

    
    
