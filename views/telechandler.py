import logging
import config
from utils.authenticated import required_login
from utils.response_code import RET, error_map
from utils.sqlUtils import sqlexecute, sql_Query_All
from views.basehandler import BaseHandler


class AddContactsHandler(BaseHandler):

    @required_login
    def post(self):
        user_id = self.token.data["user_id"]
        friend_id = self.json_args.get("friendId")
        try:
            sqlexecute(self.db,
                       """INSERT INTO tb_friends(user_id, friend_id) 
                       SELECT %(user_id)s, %(friend_id)s FROM DUAL
                       WHERE NOT EXISTS(SELECT id FROM tb_friends
                       WHERE (friend_id = %(friend_id)s AND user_id = %(user_id)s ) OR 
                       (friend_id = %(user_id)s AND user_id = %(friend_id)s ))""",
                       {"user_id": user_id, "friend_id": friend_id})
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, msg=error_map[RET.DBERR]))
        return self.write(dict(errcode=RET.OK, msg=error_map[RET.OK]))


class ALLContactsHandler(BaseHandler):

    @required_login
    def get(self):
        user_id = self.token.data['user_id']
        try:
            res = sql_Query_All(self.db,
                          """SELECT user_id, nickname, password, phone, avater, signature
                           FROM tb_user WHERE user_id =
                          (SELECT friend_id FROM tb_friends WHERE user_id = %s)""", user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, msg=error_map[RET.DBERR]))
        return self.write(dict(errcode=RET.OK, msg=error_map[RET.OK], data=res))


class RemoveContactsHandler(BaseHandler):

    @required_login
    def post(self):
        user_id = self.token.data["user_id"]
        friend_id = self.json_args.get("friendId")
        try:
            sqlexecute(self.db,
                       """DELETE FROM tb_friends WHERE 
                       ( user_id = %(user_id)s AND friend_id = %(friend_id)s ) or 
                       (user_id = %(friend_id)s AND friend_id = %(user_id)s )""",
                       {"user_id": user_id, "friend_id": friend_id})
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, msg=error_map[RET.DBERR]))
        return self.write(dict(errcode=RET.OK, msg=error_map[RET.OK]))
