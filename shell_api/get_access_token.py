# -*- coding: utf-8 -*-
import requests
import ssl
import time
# client_id 为官网获取的AK， client_secret 为官网获取的SK
#有效期为30天
host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % ("oWi6v83wEaKxRmq7vNRVGqbi","In3yd32SaBTrzhvxijMTNz9P7u72ZCt4")
r=requests.get(host)
json=r.json()
access_token=json['access_token'] #得到access_token
expires_in=json['expires_in'] #剩余秒数
ts=int(time.time())+expires_in #截至日期时间戳
lt=time.localtime(ts) #转成本地时间
dt=time.strftime("%Y-%m-%d %H:%M:%S",lt) #变成可视化的时间
print("access_token:%s\n有效期至：%s" % (access_token,dt))
