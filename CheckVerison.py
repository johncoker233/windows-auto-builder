
import subprocess
import http.client
import os
import re
import requests
import json
import sys
BEARER = os.environ['BEARER']
ACCOUNT_IDENTIFIER = os.environ['ACCOUNT_IDENTIFIER']
NAMESPACE_IDENTIFIER = os.environ['NAMESPACE_IDENTIFIER']


url = 'https://api.uupdump.net/listid.php?search=Windows%2011,%20version%2023H2'

search_term = "Windows 11, version 23H2"
response = requests.get(url)

data = json.loads(response.text)

for build in data['response']['builds'].values():
  if build['arch'] == 'amd64':
    print(build['uuid'])
    updateid = build['uuid']
    title = build['title']
    build = build['build']
    break

conn = http.client.HTTPSConnection("api.cloudflare.com")

headers = {
    'Content-Type': "application/json",
    'Authorization': f"Bearer {BEARER}"
}

try:
    # 构建 Cloudflare API 请求路径
    path = f"/client/v4/accounts/{ACCOUNT_IDENTIFIER}/storage/kv/namespaces/{NAMESPACE_IDENTIFIER}/values/system"
    conn.request("GET", path, headers=headers)
    
    res = conn.getresponse()
    
    if res.status != 200:
        print(f"Error: Cloudflare API request failed with status {res.status}")
        exit(1)
    
    data = res.read()
except Exception as e:
    print(f"Error making Cloudflare API request: {e}")
    exit(1)


data = data.decode('utf-8') # 解码成普通字符串

if data == updateid:
    sys.exit(1)
output_file = os.path.join(os.getcwd(), 'updateId.txt')
with open(output_file, 'w') as f:
    f.write(updateid)
output_file = os.path.join(os.getcwd(), 'title.txt')
with open(output_file, 'w') as f:
    f.write(title)
output_file = os.path.join(os.getcwd(), 'build.txt')
with open(output_file, 'w') as f:
    f.write(build)