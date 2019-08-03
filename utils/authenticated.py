import functools


def required_login(fun):
    # 保证被装饰的函数对象的__name__不变
    @functools.wraps(fun)
    def wrapper(request_handler_obj, *args, **kwargs):
        # 调用get_current_user方法判断用户是否登录
        if not request_handler_obj.get_current_user():
            # session = Session(request_handler_obj)
            # if not session.data:
            request_handler_obj.write(dict(errcode=101, errmsg="用户未登录"))
        else:
            fun(request_handler_obj, *args, **kwargs)

    return wrapper
