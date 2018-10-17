from functools import wraps
from flask import session,redirect,url_for
from config import FRONT_USER_ID

def request_login(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        if FRONT_USER_ID in session:
            return fun(*args,**kwargs)
        else:
            return redirect(url_for('front.login'))
    return inner