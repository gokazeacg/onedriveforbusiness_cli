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
    global tenant_ID, client_id, client_secret, access_token, refresh_token
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
    return access_token

def get_id(path):
    global headers
    url = "https://graph.microsoft.com/v1.0/me/drive/"+path
    retur = json.loads(requests.get(url, headers=headers).text)
    if requests.get(url, headers=headers).status_code != 200:
        print(requests.get(url, headers=headers).text)
    return retur['id']

if float(sol) + 1800 < time.time():
    access_token = refresh()

headers = {'Authorization': 'Bearer '+access_token}
print('輸入資料夾路徑(根目錄"root:")：',end='')
path = input()
path = path.split('/')
name = path[-1]
del path[-1]
path = '/'.join(path)
if path == 'root:':
    path = 'root'
url = 'https://graph.microsoft.com/v1.0/me/drive/items/'+get_id(path)+'/children'
data = {"name": name, "folder": { },"@microsoft.graph.conflictBehavior": "rename"}
re = requests.post(url=url, headers=headers, json=data)
if re.status_code == 201:
    print(json.loads(re.text)['webUrl'])
else:
    print(re.text)