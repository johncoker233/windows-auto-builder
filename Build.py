import os
import subprocess
import patoolib
import configparser
import tempfile
import wmi
import hashlib
temp_dir = tempfile.gettempdir()
DOWNLOAD_PATH = os.getcwd()
extract_dir = os.path.join(temp_dir, 'ISO')

if not os.path.exists(temp_dir):
  os.makedirs(temp_dir)

# 设置变量

files = os.listdir(temp_dir)

for file in files:
    if os.path.splitext(file)[1] == ".ISO":
        break

ISO = temp_dir + '\\' + file
# 解压ISO  
patoolib.extract_archive(ISO, outdir=extract_dir)

# 挂载WIM文件
wim_file = os.path.join(extract_dir, r'sources\install.wim')
mount_dir = os.path.join(temp_dir, 'Mount')
if not os.path.exists(mount_dir):
  os.makedirs(mount_dir)

subprocess.run(["dism", "/Mount-Wim", "/WimFile:" + wim_file, "/index:1", "/MountDir:" + mount_dir])


config = configparser.ConfigParser()
config.read('Pack.ini', encoding='utf-8')

PackName = config["Config"]["Name"]
To = config["Config"]["To"]

if To == "MountDir":
    To = mount_dir
if To == "Root":
    To = DOWNLOAD_PATH
if To == "Temp":
    To = temp_dir

File = DOWNLOAD_PATH + '\\' + PackName
if not os.path.exists(File):
    raise FileNotFoundError(f'{File} 文件不存在')

# 计算MD5

patoolib.extract_archive(File, outdir=To)

path = os.path.join(To, 'Build.cmd')
if os.path.exists(path):
    subprocess.run([path])
else:
    print(f"File {path} not found.")

if os.path.exists(path):
    os.remove(path)
    print(f"File '{path}' deleted.")
else:
    print(f"File '{path}' does not exist.")