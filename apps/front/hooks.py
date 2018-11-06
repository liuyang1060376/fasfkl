from apps.front.views import bp
from flask import session,g,render_template
from apps.front.models import Front_user
from apps.models import  BoardModel
import config


#钩子函数，把当前登录用户和所有板块存入g中
@bp.before_request
def beforerequest():
    if config.FRONT_USER_ID in session:
        front_user_id=session.get(config.FRONT_USER_ID)
        user=Front_user.query.get(front_user_id)
        if user:
            g.front_user=user
            print(g.front_user)
    boards=BoardModel.query.all()
    if boards:
        g.boards=boards

# 自定义http状态码
@bp.errorhandler(404)
def errorhand(error):
    return render_template('cms/error.html')