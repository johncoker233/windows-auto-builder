import os
import tempfile
import subprocess

DOWNLOAD_PATH = os.getcwd()
system_drive = os.getenv('SystemDrive')
temp_dir = tempfile.gettempdir()

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

extract_dir = os.path.join(temp_dir, 'ISO')
wim_file = os.path.join(extract_dir, r'sources\install.wim')
mount_dir = os.path.join(temp_dir, 'Mount')

# 设置变量
extract_dir = os.path.join(temp_dir, 'ISO')
ESD = os.path.join(temp_dir, 'EquaImage.esd')

# 使用 dism 打包成 WIM 文件
cmd = 'wimlib-imagex.exe capture ' + mount_dir + ' ' + ESD + ' ' + '--check --solid'  
subprocess.run(cmd, shell=True)
