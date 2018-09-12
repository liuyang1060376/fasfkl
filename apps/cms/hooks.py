from .views import bp
from flask import Blueprint,session,g
from config import CMS_USER_ID
from apps.cms.models import CMS_user
@bp.before_request      #使用钩子函数从session中获取用户的资料
def before_request():
    if CMS_USER_ID in session:    #如果在session中存在cms_user_id这个变量
        id=session.get(CMS_USER_ID) #那么从session中取出这个变量
        user=CMS_user.query.get(id)          #从session中取出这个用户的信息存放在g中
        if user:
            g.cms_user=user
