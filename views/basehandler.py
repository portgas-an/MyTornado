# coding:utf-8
from tornado.web import RequestHandler
from utils.token import Token
import json


class BaseHandler(RequestHandler):
    # handler基类
    @property
    def db(self):
        return self.application.db


    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body.decode('utf-8'))
        else:
            self.json_args = {}
            for key in self.request.arguments:
                self.json_args[key] = self.get_argument(key)

    def write_error(self, status_code, **kwargs):
        pass

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json;charset=UTF-8")

    def initialize(self):
        pass

    def on_finish(self):
        pass

    def get_current_user(self):
        self.token = Token(self)
        return self.token.data
