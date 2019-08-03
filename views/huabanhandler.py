import logging
from utils.authenticated import required_login
from utils.response_code import RET, error_map
from views.basehandler import BaseHandler
from utils.sqlUtils import sql_Query_All
import json


class IndexHuabanHandler(BaseHandler):

    @required_login
    def post(self):
        pin_id = self.json_args.get("pinId")
        if pin_id:
            res = sql_Query_All(self.db, """SELECT * FROM tb_pin WHERE pin_id = %s LIMIT 20""", pin_id)
        else:
            try:
                res = sql_Query_All(self.db,
                              """SELECT * FROM tb_pin WHERE 
                              pin_id >= ((SELECT MAX(pin_id) FROM tb_pin)-
                              (SELECT MIN(pin_id) FROM tb_pin)) * RAND() + 
                              (SELECT MIN(pin_id) FROM tb_pin)  LIMIT 20""")
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR, msg=error_map[RET.DBERR]))
            for data in res:
                data["content"] = json.loads(data["content"], encoding="uft-8")
        return self.write(dict(errcode=RET.OK, msg=error_map[RET.OK], data=res))


class TypeHuabanHandler(BaseHandler):

    @required_login
    def post(self):
        pin_id = self.json_args.get("pinId")
        pin_type = self.json_args.get("type")
        if pin_id:
            res = sql_Query_All(self.db, """SELECT * FROM tb_pin WHERE pin_id = %s AND pin_type = %s LIMIT 20""", (pin_id, pin_type))
        else:
            try:
                res = sql_Query_All(self.db,
                              """SELECT * FROM tb_pin_type WHERE 
                               pin_type = %s  LIMIT 1,20""", pin_type)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR, msg=error_map[RET.DBERR]))
            for data in res:
                data["content"] = json.loads(data["content"], encoding="uft-8")
        return self.write(dict(errcode=RET.OK, msg=error_map[RET.OK], data=res))
