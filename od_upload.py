import requests
import json
from urllib import parse
from urllib.parse import unquote
import os
import re
from od_refresh_token import refresh

if os.name == 'posix':
    storag = '~/.od_cli/.token'
elif os.name == 'nt':
    storag = os.getenv('USERPROFILE')+'\AppData\Local\.token'
f = open(storag,'r')
fread = f.read()
f.close()
sol = fread.split(',')[0]
tenant_ID = fread.split(',')[1]
client_id = fread.split(',')[2]
client_secret = fread.split(',')[3]
access_token = fread.split(',')[4]
refresh_token = fread.split(',')[5]

if float(sol) + 3200 < time.time():
    access_token = refresh()

headers = {'Authorization': 'Bearer '+access_token}
pice = 0
pice2 = 319
split = 320
print('輸入要上傳的檔案名稱：',end='')
file = input()
url = 'https://graph.microsoft.com/v1.0/users/me/drive/items/root:/'+file+':/createUploadSession'
uploadurl = json.loads(requests.post(url,headers = headers).text)['uploadUrl']
uploadfile = open(file,'rb')
size = os.path.getsize(file)

for i in range(0,(size//320)):
    headers = {'Authorization': 'Bearer '+content,'Content-Length': '320', 'Content-Range': 'bytes '+str(pice)+'-'+str(pice2)+'/'+str(size)}
    print(requests.put(uploadurl,data=uploadfile.read(320),headers=headers).text)
    pice = pice + split
    pice2 = pice2 + split

pice = (size//split)*split+1
pice2 = size
headers = {'Authorization': 'Bearer '+content,'Content-Length': '320', 'Content-Range': 'bytes '+str(pice)+'-'+str(pice2)+'/'+str(size)}
print(requests.put(uploadurl,data=uploadfile.read(320),headers=headers).text)
