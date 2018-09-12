from flask import Blueprint, request, render_template, session, redirect, url_for, g,views,jsonify
from apps.cms.forms import Cms_login_verify,Cms_resetpwd_verify,Cms_resetemail_verify
from exts import db

from apps.cms.decorators import Request_login
from apps.cms.models import CMS_user
from config import CMS_USER_ID
bp=Blueprint('cms',__name__,url_prefix='/cms')  #创建蓝图


@bp.route('/')                              #后台界面首页
@Request_login
def index():
    return render_template("cms/CMS_index.html")

@bp.route('/cms_off/')    #注销登录
@Request_login         #必须登录才能访问
def cms_off():
    del session[CMS_USER_ID]
    return redirect(url_for("cms.login"))

@bp.route('/login/',methods=['GET','POST'])                 #后台登录系统
def login(message='none'):
    if request.method=='GET':
        return render_template('cms/CMS_login.html')        #如果是GET请求,返回登录界面
    else:
        form=Cms_login_verify(request.form)         #验证前台输入的数据是否合法
        if form.validate():                         #如果合法
            email=form.email.data
            passwd=form.passwd.data
            remember=form.remember.data
            user=CMS_user.query.filter(CMS_user.email==email).first()     #获取这个用户
            # print(user.check_password(raw_passwd=passwd))
            if user:
                if user.check_password(raw_passwd=passwd):     #如果用户名和密码都正确
                    session[CMS_USER_ID]=user.id
                    if remember:                    #如果勾选了记住密码
                        session.permanent=True    #设置SESSION的过期时间时间【默认是30天，可以设置PERMANENT_SESSION_LIFETIME修改】

                    return redirect(url_for("cms.index"))
                else:
                    print('{0}用户的密码错误'.format(user.username))
                    return render_template("cms/CMS_login.html", message="用户账号或者密码输入错误")
            else:
                print('用户名输入错误')
                return render_template("cms/CMS_login.html", message="用户账号或者密码输入错误")
        else:
            print(form.errors)
            return render_template("cms/CMS_login.html",message="信息不正确")

@bp.route('/profile/')                              #个人中心
@Request_login
def profile():
    return render_template("cms/CMS_profile.html")

#基于方法调度的类视图
'''code 200(输入正确，修改密码成功)
   code 400(密码错误，修改密码失败)
   code 403(表单验证失败，用户输入信息格式不正确)
  '''
class ResetPwd_View(views.MethodView):
    decorators=[Request_login]          #装饰器（必须登录才可访问）
    def _render(self,address):              #把render_template封装成一个方法
        return  render_template(address)
    def get(self):      #使用get请求
        return self._render("cms/CMS_resetpwd.html")
    def post(self):      #使用post请求
        form=Cms_resetpwd_verify(request.form)  #对接收到的数据进行验证，查看数据格式是否合法
        if form.validate():
            oldpasswd=form.oldpasswd.data        #从验证表单中获取到（老新）密码
            newpasswd=form.newpasswd.data
            if g.cms_user.check_password(oldpasswd):    #旧密码等于数据库的密码，验证通过返回成功
                g.cms_user.passwd=newpasswd
                db.session.commit()
                return jsonify({'code':200,'message':''})
            else:
                return jsonify({'code':400,'message':'密码输入错误'})
        else:
            message=form.errors.popitem()[1][0]    #弹出表单验证错误的第一条错误提示
            return jsonify({'code':403,'message':message})
bp.add_url_rule('/resetpwd/',view_func=ResetPwd_View.as_view('resetpwd'))



'''
   code 200（修改密码成功）
   code 400 (验证码和邮箱不匹配)
'''
class Resetemail_View(views.MethodView):                #重置邮箱
    def get(self):
        return render_template('cms/CMS_resetemail.html')
    def post(self):
        form=Cms_resetemail_verify(request.form)
        if form.validate():
            email=form.email.data
            g.cms_user.email=email
            db.session.commit()
            return jsonify({'code':200,'message':'邮箱修改成功'})
        else:
            message=form.errors.popitem()[1][0]
            return jsonify({'code':400,'message':message})
bp.add_url_rule('/resetemail/',view_func=Resetemail_View.as_view('resetemail'))
