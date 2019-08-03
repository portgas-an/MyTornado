# -*- coding:utf-8
import logging
from random import randint
from utils.response_code import RET, error_map
from utils.token import Token
from views.basehandler import BaseHandler
from utils.sqlUtils import sqlexecute, sql_Query_One


class RegisterHandler(BaseHandler):
    def post(self):
        phone = self.json_args.get("mobile")
        sms_code = self.json_args.get("phonecode")
        password = self.json_args.get("password")
        if not all((phone, sms_code, password)):
            return self.write(dict(errcode=RET.PARAMERR, msg=error_map[RET.PARAMERR]))
        real_code = self.redis.get("sms_code_%s" % phone).decode('utf-8')
        if real_code != str(sms_code):
            return self.write(dict(errcode="2", msg="验证码无效"))
        try:
            # 会返回生成的主键
            res = sqlexecute(self.db, """insert into tb_user(nickname, phone,password) values(%s, %s, %s)""",
                             (phone, phone, password))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode="3", msg=error_map[RET.DATAEXIST]))
        try:
            self.session = Token(self)
            self.session.data['user_id'] = res
            self.session.data['nickname'] = phone
            self.session.data['phone'] = phone
            self.session.save()
        except Exception as e:
            logging.error(e)
            print(e)
        self.write(dict(errcode=RET.OK, msg=error_map[RET.OK]))


class LoginHandler(BaseHandler):
    def post(self):
        phone = self.json_args.get("mobile")
        password = self.json_args.get("password")
        if not all((phone, password)):
            return self.write(dict(errcode=RET.PARAMERR, msg=error_map[RET.PARAMERR]))
        res = sql_Query_One(self.db,
                       "select * from tb_user where phone=%s", phone)
        if res and res["password"] == str(password):
            try:
                self.session = Token(self)
                self.session.data['user_id'] = res["user_id"]
                self.session.data['nickname'] = res["nickname"]
                self.session.data['phone'] = res["phone"]
                self.session.save()
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.LOGINERR, msg=error_map[RET.LOGINERR]))
            res.pop("password")
            return self.write(dict(errcode=RET.OK, msg=error_map[RET.OK], data=res))
        else:
            return self.write(dict(errcode='2', msg="手机号或密码错误"))


class PhoneCodeHandler(BaseHandler):
    """"""

    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile")
        if not all(mobile):
            return self.write(dict(errcode=RET.PARAMERR, msg=error_map[RET.PARAMERR]))
        # 成功发送信息,失败返回错误信息
        sms_code = "%04d" % (randint(0, 9999))
        try:
            self.redis.setex("sms_code_%s" % mobile, 3600, sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, msg="生成验证码错误"))
        # 发送短信
        return self.write(dict(errcode=RET.OK, msg=error_map[RET.OK], data=sms_code))

