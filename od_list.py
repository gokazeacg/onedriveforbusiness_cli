import requests
import json
from urllib import parse
import os

print('輸入目錄 (租用戶) 識別碼：',end='')
tenant_ID = str(input())
print('輸入應用程式 (用戶端) 識別碼：',end='')
client_id = str(input())
print('輸入用戶端密碼：',end='')
client_secret = str(input())

def get_token():
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    url = 'https://login.microsoftonline.com/'+tenant_ID+'/oauth2/v2.0/token'
    FormData = {'client_id':client_id,'scope':'.default','client_secret':client_secret,'grant_type':'client_credentials'}
    data = parse.urlencode(FormData)
    content = requests.post(url=url, headers=HEADERS, data=data).text
    content = json.loads(content)['access_token']
    print('你的金鑰為：'+content)
    return content

if '.token' in os.listdir():
    file = open('./.token','r')
    content = file.read()
    file.close()
else:
    file = open('./.token','w')
    content = get_token()
    file.write(content)
    file.close()

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
