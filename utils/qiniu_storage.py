# -*- coding: utf-8 -*-

import qiniu.config
import logging

from qiniu import Auth, put_data, etag, urlsafe_base64_encode


#需要填写你的 Access Key 和 Secret Key
access_key = 'rdWcd00BBpTfqUoCBtubQ0qslneEZJ2a9EojN0ly'
secret_key = 'V6ZBR6pidep_30TByUccfzFOsNSn7GBERUnmcfoZ'


def storage(file_data):
    try:
        # 构建鉴权对象
        q = Auth(access_key, secret_key)

        # 要上传的空间
        bucket_name = 'myproject'

        # 上传到七牛后保存的文件名
        # key = 'my-python-logo.png';

        # 生成上传 Token，可以指定过期时间等

        token = q.upload_token(bucket_name)

        # 要上传文件的本地路径
        # localfile = './sync/bbb.jpg'
        # ret, info = put_file(token, key, localfile)
        ret, info = put_data(token, None, file_data)
    except Exception as e:
        logging.error(e)
        raise e
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)

    if 200 == info.status_code:
        return ret["key"]
    else:
        raise Exception("上传失败")
