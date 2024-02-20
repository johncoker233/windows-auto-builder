# Windows自动构建与对象存储上传

## 简介
自动构建最新版本的Windows并将其上传到对象存储服务。通过GitHub Action每隔一段时间自动检查构建。完全免费.使用WTDR离线封装

## 使用方法
### 1. Fork存储库
首先，使用此模版创建一个新的存储库到您自己的GitHub帐户中。(您可以设置为私密)

### 3.设置Cloudflare KV
在Cloudlare Dashboard中侧边栏的Workers 和 Pages 的KV选项卡，点击创建命名空间，取个名字。然后复制命名空间的ID和右侧的帐户 ID

### 4.创建存储库（不一定用R2，有免费10GB额度）
Cloudlare Dashboard中侧边栏的R2选项卡，点击创建存储桶，取个名字。其他默认就好。先点击右边的管理 R2 API 令牌。创建API令牌。**权限选择对象读和写**。点击创建API令牌，访问密钥 ID
就是AWS_ACCESS_KEY_ID。机密访问密钥就是AWS_SECRET_ACCESS_KEY。请保存好。

然后点击刚刚创建的存储桶。转到"设置"。S3 API去掉后面的存储桶名和斜杠就是S3_ENDPOINT。
### 4. 添加机密信息
在GitHub上导航到您复制的存储库，转到“Settings”选项卡。在左侧边栏中，点击“Secrets”，然后点击“New repository secret”。添加以下机密信息及其相应的值：

- **ACCOUNT_IDENTIFIER**：您的Cloudflare帐户标识符。
- **API_KEY**：[您的Cloudlfare API密钥](https://dash.cloudflare.com/profile/api-tokens（Global API Key）
- **AWS_ACCESS_KEY_ID**：您的AWS访问密钥ID。
- **AWS_SECRET_ACCESS_KEY**：您的AWS秘密访问密钥。
- **BEARER**：[您的Cloudlfare令牌](https://dash.cloudflare.com/profile/api-tokens)
- **BUCKET_NAME**：您对象存储桶的名称。
- **EMAIL**：您的电子邮件地址。
- **NAMESPACE_IDENTIFIER**：您的命名空间标识符。
- **REGION_NAME**：您对象存储的区域名称。
- **S3_ENDPOINT**：您S3兼容对象存储服务的终端点。
- **ESD_NAME**:ESD镜像名称

确保保持这些机密信息的机密性，不要公开它们。

### 5.自定义
1. 您可以自定义操作系统部署辅助工具。您可以将所需文件**打包成7z**（务必！！否则可能无法解压！！），并编辑Pack.ini。Name指的是7z的文件名（带后缀）。To指的是释放位置（Temp是临时目录，Root指的是python工作目录，MountDir指的是挂载目录（install.wim的释放目录）。您可以在**7z压缩包中自带Build.cmd**程序会自动运行，然后删除。建议您修改后测试一下第一版

2. 对于GitHub Action的定时触发,可以使用schedule语法来指定定时执行的时间。常见的schedule语法有以下几种:

- 每小时执行一次:

```
schedule:
  - cron: '0 * * * *'
```

- 每天凌晨1点执行一次:

```
schedule:
  - cron: '0 1 * * *' 
```

- 每周一早上9点执行一次:

```
schedule:
  - cron: '0 9 * * 1'
```

- 每月1日和15日执行一次:

```
schedule:
  - cron: '0 0 1,15 * *'
```

- 每天中午12点执行一次:

```
schedule: 
  - cron: '0 12 * * *'
```

cron表达式允许自定义更复杂的定时方案。主要组成为5个空格分隔的字段,分别代表分钟、小时、月份中的第几天、月份、星期中的第几天。星号表示每月/每天/每周等全选。

您可以在.github/workflows/build.yml中修改

### 6. 等待部署

一旦配置完毕，Action会每隔6小时运行一次。您无法手动运行

### **如果此项目对您有帮助，就给个star支持一下吧xD**
# 致谢
- [WTDR](https://wtdr.whatk.me)
- [ChatGPT](https://chat.openai.com)  [Debug]
- [Windsys Project](https://windsys.win)  [Idea]
- [Microsoft](https://microsoft.com)
- [boto3](https://github.com/boto/boto3)
- [patool](https://pypi.org/project/patool/)

# 免责声明
Windows 操作系统版权归属于 Microsoft，该项目与 Microsoft 无关，该项目也不是 Microsoft 旗下网站。
本项目的最终目的并非盈利，只是为更好的推广 Windows 生态，并且使 Windows 系统定制更便捷，并且使其更方便使用。
