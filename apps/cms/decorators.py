from flask import session,redirect,url_for
from functools import wraps
from config import CMS_USER_ID
def Request_login(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        if CMS_USER_ID in session:
            return fun(*args,**kwargs)
        else:
            return redirect(url_for("cms.login"))
    return inner