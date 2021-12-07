import requests
import json
from urllib import parse
import os
import time

f = open('.token','r')
fread = f.read()
f.close()
sol = fread.split(',')[0]
tenant_ID = fread.split(',')[1]
client_id = fread.split(',')[2]
client_secret = fread.split(',')[3]
access_token = fread.split(',')[4]
refresh_token = fread.split(',')[5]
if float(sol) + 1600 < time.time():
    sol = time.time()
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    data = 'client_id='+client_id+'&scope=https%3A%2F%2Fgraph.microsoft.com%2FFiles.ReadWrite.All%20offline_access&redirect_uri=http%3A%2F%2Flocalhost%3A4452%2F&client_secret='+client_secret+'&grant_type=refresh_token&refresh_token='+refresh_token
    retur = json.loads(requests.post(url=url, headers=HEADERS, data=data).text)
    access_token = retur['access_token']
    #print('你的訪問令牌為：'+access_token)
    refresh_token = retur['refresh_token']
    #print('你的刷新令牌為：'+refresh_token)
    x = str(sol)+','+tenant_ID+','+client_id+','+client_secret+','+access_token+','+refresh_token
    f = open('.token','w')
    f.write(x)
    f.close()