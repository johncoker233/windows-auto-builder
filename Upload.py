import os
import boto3
import tempfile
import json
import requests
import hashlib
# 从环境变量中获取参数
BEARER = os.environ['BEARER']
ACCOUNT_IDENTIFIER = os.environ['ACCOUNT_IDENTIFIER']
NAMESPACE_IDENTIFIER = os.environ['NAMESPACE_IDENTIFIER']
EMAIL = os.environ['EMAIL']
API_KEY = os.environ['API_KEY']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
REGION_NAME = os.environ['REGION_NAME']
BUCKET_NAME = os.environ['BUCKET_NAME']
S3_ENDPOINT = os.environ['S3_ENDPOINT']
esd_filename = os.environ['ESD_NAME']
# 获取临时目录路径
temp_dir = tempfile.gettempdir()

# 在临时目录下搜索ESD文件
esd_filename = 'EquaImage.esd'
esd_path = ''
for root, dirs, files in os.walk(temp_dir):
    if esd_filename in files:
        esd_path = os.path.join(root, esd_filename)
        print(f"Found ESD file at {esd_path}")
        break

if esd_path:
    # 创建S3客户端
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=REGION_NAME,
                      endpoint_url=S3_ENDPOINT)

    # 上传文件到S3
    s3.upload_file(esd_path, BUCKET_NAME, 'system/'+esd_filename)

    print("Uploaded ESD file to S3")
else:
    print(f"ESD file {esd_filename} not found in {temp_dir}")



# 从文件中读取版本信息
version_file = os.path.join(os.getcwd(), 'updateId.txt')
with open(version_file, 'r', encoding='utf-8') as f:
    updateId = f.read()

version_file = os.path.join(os.getcwd(), 'title.txt')
with open(version_file, 'r', encoding='utf-8') as f:
    title = f.read()

version_file = os.path.join(os.getcwd(), 'build.txt')
with open(version_file, 'r', encoding='utf-8') as f:
    build = f.read()

md5 = hashlib.md5()
with open(esd_path, 'rb') as f:
    data = f.read()
    md5.update(data)

archive_md5 = md5.hexdigest()
print(f'MD5: {archive_md5}')
# 发送版本信息到 Cloudflare KV
url = "https://api.cloudflare.com/client/v4/accounts/{account_identifier}/storage/kv/namespaces/{namespace_identifier}/bulk"
key = "system"
headers = {
    "Authorization": f"Bearer {BEARER}",
    "X-Auth-Email": f"{EMAIL}",
    "X-Auth-Key": f"{API_KEY}"
}
data = [
    {
        "base64": False,
        "expiration": None,
        "expiration_ttl": None,
        "key": key,
        "metadata": {},
        "value": updateId
    }
]
response = requests.put(
    url.format(account_identifier=ACCOUNT_IDENTIFIER, namespace_identifier=NAMESPACE_IDENTIFIER),
    json=data,
    headers=headers
)

# 处理 Cloudflare KV 的响应
if response.status_code == 200:
    print("Key-value pair written successfully.")
else:
    print(f"Error: {response.status_code} - {response.json()}")
