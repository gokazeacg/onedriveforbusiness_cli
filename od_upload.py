import requests
import json
from urllib import parse
from urllib.parse import unquote
import os
import re

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

def download_file(url):
    d = requests.get(url, stream=True, headers=headers).headers['content-disposition']
    local_filename = re.findall('filename="(.+)"', d)[0]
    local_filename = unquote(local_filename)
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename


def get_token():
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    url = 'https://login.microsoftonline.com/'+tenant_ID+'/oauth2/v2.0/token'
    FormData = {'client_id':'5d7f86fe-e1b7-4d6e-a966-56c5ee83449e','scope':'.default','client_secret':'LCU7Q~OFdIOt1.gZoyZj2N4Rwy.f_Z83u94JP','grant_type':'client_credentials'}
    data = parse.urlencode(FormData)
    content = requests.post(url=url, headers=HEADERS, data=data).text
    content = json.loads(content)['access_token']
    #print('你的金鑰為：'+content)
    return content

if float(sol) + 3600 < time.time():
    access_token = refresh()

headers = {'Authorization': 'Bearer '+content}
url = 'https://graph.microsoft.com/v1.0/users'
usersjson = json.loads(requests.get(url, headers=headers).text)
x = 1
#print('使用者列表：')
for i in usersjson['value']:
    #print(str(x)+'.'+i['mail'])
    x += 1
    #print(i['id'])


#print('選擇使用者：',end='')
#GUIDx = int(input())
GUIDx = 4
GUID = usersjson['value'][GUIDx-1]['id']

pice = 0
pice2 = 319
split = 320
print('輸入要上傳的檔案名稱：',end='')
file = 'test.rar'
url = 'https://graph.microsoft.com/v1.0/users/'+GUID+'/drive/items/root:/'+file+':/createUploadSession'
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