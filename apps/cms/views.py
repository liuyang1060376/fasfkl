from flask import (
                   Blueprint,
                   request,
                   render_template,
                   session,
                   redirect,
                   url_for,
                   g,views,
                   jsonify,
                   abort
                   )
from apps.cms.forms import (
                            Cms_login_verify,
                            Cms_resetpwd_verify,
                            Cms_resetemail_verify,
                            Add_banner_verify,
                            Update_banner_verify,
                            Add_boarder_verify,
                            Update_boarder_verify,
                            Agoodpost_verify,
                            Delgoodpost_verify,
                            Delpost_verify
                            )
from exts import db
from apps.cms.decorators import Request_login,Request_Permission
from apps.cms.models import CMS_user, Permission
from apps.models import BoardModel,PostModel
from config import CMS_USER_ID
from apps.front.models import Front_user
from apps.models import Banner_Model
from flask_paginate import get_page_parameter,Pagination
from datetime import datetime
from flask_paginate import Pagination
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



@bp.route('/profile/')                              #个人中心
@Request_login
def profile():
    return render_template("cms/CMS_profile.html")

#基于方法调度的类视图
'''code 200(输入正确，修改密码成功)
   code 400(密码错误，修改密码失败)
   code 403(表单验证失败，用户输入信息格式不正确)
  '''
class ResetPwd_View(views.MethodView):                  #修改密码
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


@bp.route('/boarder/')      #板块管理
@Request_Permission(Permission.BOARDER)
def boarder():
    page=request.args.get('page',default=1)
    page=int(page)
    start=(page-1)*8
    end=(page+8)
    boards=BoardModel.query.order_by(BoardModel.id.desc()).slice(start,end)
    pagination=Pagination(bs_version=3,page=page,total=BoardModel.query.count())
    print(pagination)
    contents={
        'boards':boards,
        'pagination':pagination
    }
    return render_template('cms/CMS_boarder_manage.html',**contents)


'''code 200(输入正确，修改密码成功)
   code 403(表单验证失败，用户输入信息格式不正确)
  '''
@bp.route('/addboard/',methods=['POST'])            #添加板块
def addboard():
    form=Add_boarder_verify(request.form)          #从接受用户传递过来的参数
    if form.validate():                             #验证用户输入格式是否正确
        img_url=form.img_url.data                   #从验证表单中取到数据
        name=form.name.data
        intr=form.intr.data
        notice=form.intr.data
        board=BoardModel(img_url=img_url,name=name,intr=intr,notice=notice)
        db.session.add(board)
        db.session.commit()
        return jsonify({'code':200,'message':'添加成功'})

    else:
        message=form.errors.popitem()[1][0]
        return jsonify({'code':403,'message':message})

'''
code:200,更改成功
code：402,数据库不存在这个banner
code:403,用户修改的数据不符合要求
'''
@bp.route('/updateboard/',methods=['POST'])                  #更新board表信息
def updateboard():
    form=Update_boarder_verify(request.form)
    if form.validate():
        id=form.id.data
        name=form.name.data
        img_url=form.img_url.data
        intr=form.intr.data
        notice=form.notice.data
        board=BoardModel.query.filter_by(id=id).first()    #从数据库中查找这个表对应的id取出来
        if board:       #如果有这个板块，则修改板块里面的字段值，否则提示没有这个板块
            board.name=name
            board.img_url=img_url
            board.intr=intr
            board.notice=notice
            db.session.commit()
            return jsonify({'code':200,'message':'修改成功'})
        else:
            return jsonify({'code':402,'message':'不存在这个板块'})
    else:
        message=form.errors.popitem()[1][0]
        return jsonify({'code':403,'message':message})

@bp.route('/delboard/',methods=['POST'])                                #删除板块
def delboard():
    id=request.form.get('id')
    board=BoardModel.query.filter_by(id=id).first()
    if board:
        db.session.delete(board)
        db.session.commit()
        return jsonify({'code':200,'message':'删除成功'})
    else:
        return jsonify({'code':403,'message':'不存在这个板块'})



@bp.route('/cmsgroup/')     #CMS用户组管理
@Request_Permission(Permission.DEVELOP)
def cmsgroup():
    return render_template('cms/CMS_cmsgroup_manage.html')


@bp.route('/post/')         #帖子管理
@Request_Permission(Permission.POSTER)
def post():
    page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取用户传上来的是第几页
    start=(page-1)*9                                                      #起始位置
    end=start+9                                                         #结束位置
    posts=PostModel.query.all()
    total=len(posts)                                                    #统计总共多少条数据
    pagination=Pagination(bs_version=3,page=page,total=total)
    posts = PostModel.query.slice(start,end)
    content={
        'posts':posts,
        'pagination':pagination
    }
    return render_template('cms/CMS_post_manage.html',**content)


@bp.route('/commen/')        #评论管理
@Request_login
@Request_Permission(Permission.COMMENTER)
def commen():
    return render_template('cms/CMS_commen_manage.html')

@bp.route('/front/')        #前台用户管理
@Request_Permission(Permission.FRONTUSER)
def front():
    users=Front_user.query.all()        #拿到所有的前台用户
    return render_template('cms/CMS_front_manage.html',users=users)

@bp.route('/cmsuser/')       #后台用户管理
@Request_Permission(Permission.CMSUSER)
def cmsuser():
    CmsUser=CMS_user.query.all()        #拿到所有的后台用户
    return  render_template('cms/CMS_cmsuser_manage.html',CmsUser=CmsUser)






@bp.route('/addbanner/',methods=['POST'])   #添加轮播图
@Request_login
def addbanner():
    form=Add_banner_verify(request.form)                #从后台获取到前台传入的数据其中包括名称，图片地址，跳转地址和优先级，放入表单中进行验证
    if form.validate():                                 #如果验证成功
        name=form.name.data
        img_url=form.img_url.data
        link_url=form.link_url.data
        priority=form.priority.data
        banner=Banner_Model(name=name,img_url=img_url,link_url=link_url,priority=priority)
        db.session.add(banner)                          #把数据存放到数据库
        db.session.commit()
        return jsonify({'code':200,'message':'添加成功'})
    else:
        message=form.errors.popitem()[1][0]             #弹出表单的第一条验证失败的错误信息
        return  jsonify({'code':403,'message':message})


'''
code:200,更改成功
code：402,数据库不存在这个banner
code:403,用户修改的数据不符合要求
'''
@bp.route('/updatebanner/',methods=['POST'])        #更新banner图信息
def updatebanner():
    form=Update_banner_verify(request.form) #获取用户提交的修改数据
    if form:                                #如果验证用户输入的数据没有错误
        id=form.id.data                     #从验证类中获取id,name,img_ul,link_url,priority
        name=form.name.data
        img_url=form.img_url.data
        link_url=form.link_url.data
        priority=form.priority.data
        banner=Banner_Model.query.filter_by(id=id).first() #根据用户提交的id获取到这个banner图对象
        if banner:   #如果找到了这个id对应的对象，则对数据进行更改
            banner.name=name
            banner.img_url=img_url
            banner.link_url=link_url
            banner.priority=priority
            db.session.commit()
            return jsonify({'code':200,'message':'修改成功'})
        else:
            return jsonify({'code':402,'message':'没有这个轮播图'})
    else:
        message=form.errors.popitem()[1][0]
        return jsonify({'code':403,'message':message})


@bp.route('/banner/')           #轮播图管理
def banner():
    banners=Banner_Model.query.all()    #获取banner表的所有信息
    return render_template('cms/CMS_banner_manage.html',banners=banners)

@bp.route('/dbanner/',methods=['POST'])   #删除banner图
def dbanner():
    id=request.form.get('id')
    banner=Banner_Model.query.filter_by(id=id).first()
    if banner:
        db.session.delete(banner)
        db.session.commit()
        return jsonify({'code':200,'message':'删除成功'})
    else:
        return  jsonify({'code':402,'message':'不存在该轮播图'})

'''
code:200,设置精品贴成功
code:403,用户修改的数据不符合要求
'''
@bp.route('/agoodpost/',methods=['POST'])                #设置帖子为精品帖
@Request_login
def agoodpost():
    form=Agoodpost_verify(request.form)
    if form.validate():
        id=form.id.data
        post=PostModel.query.filter_by(id=id).first()  #找到这篇文章
        post.isgood=datetime.now()                      #设置该帖子为精品贴
        db.session.commit()
        return jsonify({'code':200,'message':'成功设置精品贴'})
    else:
        message=form.errors.popitem()[0][1]
        return jsonify({'code':402,'message':message})  #用户输入数据不合法

@bp.route('/delgoodpost/',methods=['POST'])                           #取消设置精品帖子
@Request_login
def delgoodpost():
    form = Delgoodpost_verify(request.form)
    if form.validate():
        id = form.id.data
        post = PostModel.query.filter_by(id=id).first()  # 找到这篇文章
        post.isgood = None  # 设置该帖子为精品贴
        db.session.commit()
        return jsonify({'code': 200, 'message': '成功取消设置精品帖子'})
    else:
        message = form.errors.popitem()[0][1]
        return jsonify({'code': 402, 'message': message})  # 用户输入数据不合法

@bp.route('/delpost/',methods=['POST'])                               #删除帖子
@Request_login
def delpost():
    form = Delpost_verify(request.form)
    if form.validate():
        id = form.id.data
        post = PostModel.query.filter_by(id=id).first()  # 找到这篇文章
        db.session.delete(post)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功'})
    else:
        message = form.errors.popitem()[0][1]
        return jsonify({'code': 402, 'message': message})  # 用户输入数据不合法



'''
code:200,更改成功
code：402,数据库不存在这个用户
code:403,用户修改的数据不符合要求
'''
@bp.route('/blockuser/',methods=['POST'])            #把用户拉黑
@Request_login
def blockuser():
    front_id=request.form.get('id')
    if front_id:
        user=Front_user.query.filter_by(id=front_id).first()
        if user:
            user.is_delete=True
            db.session.commit()
            return jsonify({'code':200,'message':'拉黑成功'})
        else:
            return jsonify({'code':402,'message':'不存在这个用户'})
    else:
        return jsonify({'code':403,'message':'用户id未输入'})
    
'''
code:200,更改成功
code：402,数据库不存在这个用户
code:403,用户修改的数据不符合要求
'''
@bp.route('/calcelblock/',methods=['POST'])                             #取消拉黑
def calcelblock():
    front_id = request.form.get('id')
    if front_id:
        user = Front_user.query.filter_by(id=front_id).first()
        if user:
            user.is_delete =False
            db.session.commit()
            return jsonify({'code': 200, 'message': '恢复成功'})
        else:
            return jsonify({'code': 402, 'message': '不存在这个用户'})
    else:
        return jsonify({'code': 403, 'message': '用户id未输入'})

@bp.route('/login/', methods=['GET', 'POST'])  # 后台登录
def login(message='none'):
    if request.method == 'GET':
        return render_template('cms/CMS_login.html')  # 如果是GET请求,返回登录界面
    else:
        form = Cms_login_verify(request.form)  # 验证前台输入的数据是否合法
        if form.validate():  # 如果合法
            email = form.email.data
            passwd = form.passwd.data
            remember = form.remember.data
            user = CMS_user.query.filter(CMS_user.email == email).first()  # 获取这个用户
            # print(user.check_password(raw_passwd=passwd))
            if user:
                if user.check_password(raw_passwd=passwd):  # 如果用户名和密码都正确
                    session[CMS_USER_ID] = user.id
                    if remember:  # 如果勾选了记住密码
                        session.permanent = True  # 设置SESSION的过期时间时间【默认是30天，可以设置PERMANENT_SESSION_LIFETIME修改】

                    return redirect(url_for("cms.index"))
                else:
                    print('{0}用户的密码错误'.format(user.username))
                    return render_template("cms/CMS_login.html", message="用户账号或者密码输入错误")
            else:
                print('用户名输入错误')
                return render_template("cms/CMS_login.html", message="用户账号或者密码输入错误")
        else:
            print(form.errors)
            return render_template("cms/CMS_login.html", message="信息不正确")

