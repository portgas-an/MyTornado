# coding:utf-8

import os
# Application配置文件
setting = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "template"),
    "cookie_secret": "lvP2jGfDTeKqm9oekT0LR+DBsSojQEYTp7ZJlKM79jo=",
    "debug": True,
}

# mysql
mysql_options = dict(
    host="127.0.0.1",
    port=3306,
    database="myproject",
    user="root",
    password="12345",
)

# redis
redis_options = dict(
    host="127.0.0.1",
)

# log
log_file = os.path.join(os.path.dirname(__file__), "logs/log")


# session有效期
session_expires = 259200

# 密码加密key
passwd_hash_key = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="

# token加密key
token_hash_key = b"nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+QW2xBB="


# 七牛外链地址
qiniu_url = "http://puexzlr4k.bkt.clouddn.com/"