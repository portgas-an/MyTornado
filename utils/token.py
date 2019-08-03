# coding:utf-8
import hashlib
import hmac
import uuid
import json
import logging
import config


class Token(object):
    """"""

    def __init__(self, request_handler_obj):

        # 先判断用户是否已经有了session_id
        self._request_handler = request_handler_obj
        self.session_id = None
        try:
            self.session_id = request_handler_obj.request.headers.get("token")
        except Exception as e:
            pass

        # 如果不存在session_id,生成session_id
        if not self.session_id:
            self.session_id = hmac.new(config.token_hash_key, uuid.uuid4().bytes, hashlib.sha256).hexdigest()
            self.data = {}
            request_handler_obj.set_header("token", self.session_id)

        # 如果存在session_id, 去redis中取出data
        else:
            try:
                json_data = request_handler_obj.redis.get("token_%s" % self.session_id)
            except Exception as e:
                logging.error(e)
                raise e
            if not json_data:
                self.data = {}
            else:
                self.data = json.loads(json_data.decode('utf-8'))

    def save(self):
        id = self.data['user_id']
        json_data = json.dumps(self.data)
        try:
            oldToken = self._request_handler.redis.get("user_%s" % id)
            if oldToken is not None:
                self._request_handler.redis.delete(oldToken)
            self._request_handler.redis.setex("user_%s" % id, config.session_expires, "token_%s" % self.session_id)
            self._request_handler.redis.setex("token_%s" % self.session_id, config.session_expires, json_data)
        except Exception as e:
            logging.error(e)
            raise e

    def clear(self):
        try:
            self._request_handler.redis.delete("token_%s" % self.session_id)
        except Exception as e:
            logging.error(e)
        self.data.clear()

