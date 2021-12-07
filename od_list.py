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

def refresh():
    sol = time.time()
    url = 'https://login.microsoftonline.com/'+tenant_ID+'/oauth2/v2.0/token'
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    FormData = {'client_id':client_id,'scope':'https://graph.microsoft.com/Files.ReadWrite offline_access','redirect_uri':'http://localhost:4452/','client_secret':client_secret,'grant_type':'refresh_token','refresh_token':refresh_token}
    data = parse.urlencode(FormData)
    retur = json.loads(requests.post(url=url, headers=HEADERS, data=data).text)
    access_token = retur['access_token']
    #print('你的訪問令牌為：'+access_token)
    refresh_token = retur['refresh_token']
    #print('你的刷新令牌為：'+refresh_token)
    x = str(sol)+','+tenant_ID+','+client_id+','+client_secret+','+access_token+','+refresh_token
    f = open('.token','r+')
    f.write(x)
    f.close()
    return access_token

if float(sol) + 3600 < time.time():
    access_token = refresh()
headers = {'Authorization': 'Bearer '+content}
url = 'https://graph.microsoft.com/v1.0/users'
usersjson = json.loads(requests.get(url, headers=headers).text)
x = 1
print('使用者列表：')
for i in usersjson['value']:
    print(str(x)+'.'+i['mail'])
    x += 1
    #print(i['id'])
print('選擇使用者：',end='')
GUIDx = int(input())
GUID = usersjson['value'][GUIDx-1]['id']
print('輸入資料夾ID(根目錄輸入"root")：',end='')
path = input()
url = 'https://graph.microsoft.com/v1.0/users/'+GUID+'/drive/items/'+path+'/children'
print(requests.get(url, headers=headers))
filelistjson = json.loads(requests.get(url, headers=headers).text)
for i in filelistjson['value']:
    if "folder" in i:
        print(i['id'],'dir',i['name'])
    else:
        print(i['id'],'file',i['name'])
