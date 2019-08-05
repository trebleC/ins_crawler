<div align="center">
  <img src="./logo.gif" height="200">
  <h2>ins-cralwler - Instagram爬虫  </h2>
</div>

[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE.txt)
[![python version](https://img.shields.io/badge/python-3.6-green?style=flat-square)]()

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/its-not-a-lie-if-you-believe-it.svg)](https://forthebadge.com)
<br><br>

# 爬取全部帖子


- [x]  正文
- [x] 点赞数
- [x] 评论数
- [x] 发帖时间
- [x] 帖子链接
- [x] 正文图片
- [x] 缩略图
- [ ] 评论
- [ ] 视频
- [ ] 正在关注

<br><br>

# 准备食用餐具
克隆
```sh
git clone https://github.com/trebleC/ins_crawler.git
```

安装依赖
```sh
pip install -r requirements.txt
```
<br><br>

# 食用方法
+ 修改用户昵称
+ 在instagram的用户主页按下F12，获取对应的query_hash以及cookie
```python
user_name = 'everyone.is.storyteller'

query_hash=' '

headers   = { 
                "cookie": " "
            }
```
+ 数据库连接默认，如需修改save_mongo(dict)中的值
```python
def save_mongo(dict):
    conn = MongoClient('localhost', 27017) #地址,端口号
    db = conn.spider    #数据库
    my_set = db.ins   #集合
```

<br><br>

# 字典
```python
edge = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]

edge["node"]["taken_at_timestamp"] #时间戳
edge["node"]["display_url"] #图片地址
edge["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"] #正文内容
edge["node"]["shortcode"] #shortcode
edge["node"]["edge_media_to_comment"]["count"] #评论数
edge["node"]["edge_media_preview_like"]["count"] #点赞数
edge["node"]["thumbnail_resources"][-1]["src"] #缩略图地址
```

[数据结构](./debug_content.json) | [debug_content.json](./debug_content.json)

<br><br>

# 截图功能

获取已经存入mongodb中的每个帖子的url，screenshot.py实现了对每篇帖子截图的功能。

- [ ] 截图功能

<br>

# 数据存储结构

在MongoDB中，每个帖子以一条信息的方式存储，每条信息的具体字段意义如下表所示：

key | 意义
-------- | --------
_id	| 帖子的时间戳
timestamp	| 帖子的时间戳
shortcode | 帖子的标识符，对于每个用户的所有帖子来说是唯一的
imgs_url | 图片地址
content | 帖子正文
counts_comment | 评论数
counts_like | 点赞数
thumbnail_url | 缩略图地址
<br><br>

对于只用过Mysql同学，下面是MongoDB安装





## Windows
```sh
下载
https://www.mongodb.com/download-center#community

按步骤安装后启动 

命令行
C:\Users\as> mongod
```
## Linux
```sh
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.0.6.tgz    # 下载
tar -zxvf mongodb-linux-x86_64-3.0.6.tgz                                   # 解压

mv  mongodb-linux-x86_64-3.0.6/ /usr/local/mongodb                         # 将解压包拷贝到指定目录
```
## 参考

[菜鸟教程](https://www.runoob.com/mongodb/mongodb-window-install.html) | [https://www.runoob.com/mongodb/mongodb-window-install.html](https://www.runoob.com/mongodb/mongodb-window-install.html)

# License

The code is available under the [MIT License](LICENSE.txt).