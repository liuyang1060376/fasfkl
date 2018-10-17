from flask import session,redirect,url_for,g,abort
from functools import wraps
from config import CMS_USER_ID
def Request_login(func):    #装饰器，用于判断每次必须登录才可以进入
    @wraps(func)
    def inner(*args,**kwargs):
        if CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for("cms.login"))
    return inner

def Request_Permission(permission):     #验证用户权限
    def outner(func):
        @wraps(func)
        def inner(*args,**kwargs):
            if g.cms_user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                abort(404)      #让他跳转到404错误界面
        return inner
    return outner


