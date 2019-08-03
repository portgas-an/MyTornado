# -*- coding:utf-8
import pymysql
import redis
import tornado.web
import tornado.ioloop
from importlib import import_module

from tornado.options import options

import config

"""
    url_router.py
"""


def include(module):
    res = import_module(module)
    urls = getattr(res, 'urls', res)
    return urls


def url_wrapper(urls):
    wrapper_list = []
    for url in urls:
        path, handles = url
        if isinstance(handles, (tuple, list)):
            for handle in handles:
                pattern, handle_class = handle
                wrap = ('{0}{1}'.format(path, pattern), handle_class)
                wrapper_list.append(wrap)
        else:
            wrapper_list.append((path, handles))
    return wrapper_list


"""
    main.py
"""


class Application(tornado.web.Application):

    def __init__(self):
        handlers = url_wrapper([
            (r"", include('views.urls')),
        ])

        tornado.web.Application.__init__(self, handlers, config.setting)
        self.db = pymysql.Connection(**config.mysql_options)
        self.redis = redis.StrictRedis(**config.redis_options)


if __name__ == "__main__":
    options.log_file_prefix = config.log_file
    Application().listen(8000, xheaders=True)
    tornado.ioloop.IOLoop.current().start()
