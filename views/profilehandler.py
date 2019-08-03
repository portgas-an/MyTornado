import logging
import config
from utils.authenticated import required_login
from utils.qiniu_storage import storage
from utils.response_code import RET, error_map
from views.basehandler import BaseHandler
from utils.sqlUtils import sqlexecute, sql_Query_One


class AvatarHandler(BaseHandler):
    """上传头像"""

    @required_login
    def post(self):
        user_id = self.token.data["user_id"]
        try:
            image = self.request.files["avatar"][0]["body"]
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.PARAMERR, msg=error_map[RET.PARAMERR]))
        try:
            image_name = storage(image)
        except Exception as e:
            logging.error(e)
            image_name = None
        if not image_name:
            return self.write(dict(errcode=RET.THIRDERR, msg=error_map[RET.THIRDERR]))
        try:
            sqlexecute(self.db,
                       "update tb_user set avater=%s where user_id=%s",
                       (config.qiniu_url+image_name, user_id))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, msg="upload failed"))
        image_url = config.qiniu_url + image_name
        return self.write(dict(errcode=RET.OK, data={"url": image_url}))


class NameHandler(BaseHandler):
    """上传个人资料"""

    @required_login
    def post(self):
        user_id = self.token.data["user_id"]
        name = self.json_args.get("name")
        signature = self.json_args.get("signature")
        try:
            sqlexecute(self.db,
                       "update tb_user set nickname=%s where user_id=%s",
                       (name, user_id))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, msg="upload failed"))
        try:
            sqlexecute(self.db,
                       "update tb_user set signature=%s where user_id=%s",
                       (signature, user_id))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, msg="upload failed"))
        return self.write(dict(errcode=RET.OK, msg="OK"))


class UserInfoHandler(BaseHandler):
    """获取个人信息"""

    @required_login
    def get(self):
        phone = self.get_current_user()["phone"]
        try:
            res = sql_Query_One(self.db,
                                "select user_id,nickname,password,phone,avater,signature from tb_user where phone=%s",
                                phone)

        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, msg=error_map[RET.DBERR]))
        return self.write(dict(errcode=RET.OK, msg=error_map[RET.OK], data=res))
