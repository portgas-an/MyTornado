"""
    json_urls.py
"""
from views.loginhandler import PhoneCodeHandler, LoginHandler, RegisterHandler
from views.profilehandler import AvatarHandler, NameHandler, UserInfoHandler
from views.huabanhandler import IndexHuabanHandler, TypeHuabanHandler
from views.telechandler import AddContactsHandler, ALLContactsHandler, RemoveContactsHandler
urls = [
    (r'/user/smscode$', PhoneCodeHandler),
    (r'/user/login$', LoginHandler),
    (r'/user/register$', RegisterHandler),
    (r'/profile/uploadavater$', AvatarHandler),
    (r'/profile/updatename$', NameHandler),
    (r'/profile/getUserInfo', UserInfoHandler),
    (r'/huaban/index', IndexHuabanHandler),
    (r'/huaban/type', TypeHuabanHandler),
    (r'/contacts/add', AddContactsHandler),
    (r'/contacts/all', ALLContactsHandler),
    (r'/contacts/remove', RemoveContactsHandler)
]
