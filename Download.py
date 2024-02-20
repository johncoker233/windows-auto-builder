import os
import tempfile
import urllib
import zipfile
import requests
import re
import subprocess

temp_dir = tempfile.gettempdir()
DOWNLOAD_PATH = os.getcwd()
version_file = os.path.join(os.getcwd(), 'updateId.txt')

def download(id, language, edition):
    try:
        request_payload = {'id': id, 'pack': language, 'edition': edition, 'autodl':"2"}
        r = requests.get("https://uupdump.net/get.php", params=request_payload, allow_redirects=True)

        d = r.headers['content-disposition']
        filename = "uupdump.zip"
        filepath = os.path.join(DOWNLOAD_PATH, filename)
        with open(filepath, 'wb') as f:
            f.write(r.content)
        return filepath
    except Exception as e:
        print("Download failed:", e)
        return None

with open(version_file, 'r', encoding='utf-8') as f:
    result = f.read()
    print("Read version from file:", result)

file_path = download(result, 'zh-cn', 'professional')
if file_path:
    print("Downloaded file to:", file_path)
else:
    print("Download failed. Exiting.")
    exit()

zip_ref = zipfile.ZipFile(file_path, "r")
zip_ref.extractall(temp_dir)
zip_ref.close()
filename = 'ConvertConfig.ini'
filepath = os.path.join(temp_dir, filename)
urllib.request.urlretrieve('https://cdn.jsdelivr.net/gh/eteam666/files/config.ini', filepath)


