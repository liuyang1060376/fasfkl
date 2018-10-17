from flask import (
                   Blueprint,
                   render_template,
                   request,
                   jsonify,
                   views,
                   session,
                   g,
                   abort
                   )
from .forms import (
                    Regist_verify,
                    Login_verify,
                    Post_verify,
                    Acommen_verify
                    )
from .models import Front_user
from apps.models import (
                        PostModel,
                        Commen_Model,
                        LikeModel,
                        Banner_Model,
                        BoardModel
                        )
from exts import db
from utils.miaodi.miaodi_sms_success import sendSuccessMessage
from .decorators import request_login
import config
from flask_paginate import get_page_parameter,Pagination
import logging


bp=Blueprint('front',__name__)

@bp.route('/')                                      #首页
def index():
    logging.error('msg')
    banners=Banner_Model.query.order_by(Banner_Model.priority.desc()).limit(5)#取出5条banner信息返回给主页，用于主页显示5条轮播图
    boards=BoardModel.query.all()                                              #取出所有板块，给前台显示出来
    goodpost=PostModel.query.filter(PostModel.isgood != None).order_by(PostModel.isgood.desc()).limit(5)#展示十条精品贴
    rposts=PostModel.query.order_by(PostModel.id.desc()).limit(5)        #取出最热的10条帖子
    content={
        'goodpost':goodpost,
        "rposts":rposts,
        'banners':banners,
        'boards':boards
    }
    return render_template('front/front_index.html',**content)



@bp.route('/regist/',methods=['GET','POST'])                                        #注册功能
def regist():
    if request.method=='GET':                                                       #GET方法
        return_to=request.referrer    #如果这个注册页面是通过用户浏览的时候点击进来的，那么获取他第三方来的url，方便注册后跳转到第三方页面
        if return_to and return_to!=request.url:
            return render_template('front/front_regist.html',return_to=return_to)
        else:
            return render_template('front/front_regist.html')
    else:                   #POST方法
        '''
        :param  username,passwd passwd2 telephone img_code
        :return: code 200  成功
                code  412  用户输入的数据不正确，或者已经注册（返回具体错误信息）
        '''
        form=Regist_verify(request.form)
        if form.validate():                 #验证表单
            username=form.username.data
            passwd=form.passwd.data
            telephone=form.mobile.data
            user=Front_user(username=username,passwd=passwd,telephone=telephone)
            db.session.add(user)
            db.session.commit()             #存放数据库，注册完成
            sendSuccessMessage(telephone,'【飞讯社区】尊敬的用户，您已成功注册为本网站会员。')
            return jsonify({'code':200,'message':'注册成功'})

        else:
            message=form.errors.popitem()[1][0]
            return jsonify({'code':412,'message':message})  #错误代码412，用户输入的数据有问题


'''412表单验证失败，弹出第一条错误信息
    200 成功
'''
class View_login(views.MethodView):                                              #登录接口
    def get(self):
        return_to = request.referrer                                            # 获取他是从哪一个网址跳转过来的
        if return_to and return_to!=request.url:                                #如果他有上一个网址，并且上一个网址不登录他自己，则返回上一个网址
            return render_template('front/front_login.html',return_to=return_to)
        else:#否则则不返还return_to
            return render_template('front/front_login.html')
    def post(self):
        form=Login_verify(request.form)                                        #把数据从表单中取出来进行验证
        if form.validate():                                                    #如果数据验证正确
            mobile = form.mobile.data  # 取出手机号
            user = Front_user.query.filter_by(telephone=mobile).first()  # 从数据库中取出这个用户
            if user.is_delete:
                return jsonify({'code':403,'message':'您的账户已经被拉黑'})
            session[config.FRONT_USER_ID]=user.id   #把用户的id取出来放在session[front_user_id]里面
            return jsonify({'code':200,'message':'登录成功'})
        else:
            message=form.errors.popitem()[1][0]
            return jsonify({'code':412,'message':message})
bp.add_url_rule('/login/',view_func=View_login.as_view('login'))


@bp.route('/front_off/',methods=['POST'])                                       #注销登录
def front_off():
    del session[config.FRONT_USER_ID]
    return jsonify({'code':200,'message':'成功注销登录'})

'''code 200   成功发表文章
   code 400   不存在该板块
   code 403(表单验证失败，用户输入信息格式不正确)
  '''

@bp.route('/apost/',methods=['GET','POST'])                                     #添加文章
@request_login
def apost():
    '''
        post:
               :param :文章的标题（title） 板块的id(id) 图片验证码（img_code） 文章内容（content）
               :return: code 200   json  发布成功
                        code 400   json  不存在该板块
                        code 403   json  传过来的数据有问题
     '''
    if request.method=='GET':
        boards=BoardModel.query.all()
        content={
            'boards':boards
        }
        return render_template('front/front_apost.html',**content)
    else:
        form=Post_verify(request.form)
        id=form.id.data
        title=form.title.data
        content=form.content.data
        print(id,title,content)
        if form.validate():
            board=BoardModel.query.get(id)
            if board:
                post=PostModel(title=title,content=content)
                post.board=board
                post.author=g.front_user
                db.session.add(post)
                db.session.commit()
                return jsonify({'code':200,'message':'发布成功'})
            else:
                return jsonify({'code':400,'message':'不存在该板块'})
        else:
            message=form.errors.popitem()[1][0]
            return jsonify({'code':403,"message":message})


@bp.route('/topic/',methods=['GET'])                                        #进入板块
def topic():
    '''
    :param  板块(id)
    :return: 进入板块
    '''
    if request.method=='GET':
        id=request.args.get('id')                                           #获取板块id，拿到具体板块信息
        board=BoardModel.query.get(id)
        page=request.args.get(get_page_parameter(),type=int, default=1)     #获取用户传上来的是第几页
        start=(page-1)*10                                                   #开始位置
        end=start+10                                                        #结束位置
        posts=PostModel.query.filter_by(board_id=id).slice(start,end)       #获取帖子从起始位置到结束位置的帖子阶段的帖子
        pagination=Pagination(bs_version=3,page=page, total=PostModel.query.filter_by(board_id=id).count())          #创建分页对象
        content={
            'board':board,
            'posts':posts,
            'pagination':pagination
        }
        return render_template('front/front_board.html',**content)




@bp.route('/pdetial/',methods=['GET'])                                      #帖子详情
def pdetial():
    '''
    :param:  帖子的id(id)
    :return: 帖子的详情,
            帖子有问题，跳转到404
    '''
    id=request.args.get('id')                                              #获取用户点击的是哪一篇帖子
    if id:
        post=PostModel.query.filter_by(id=id).first()                      #查找这篇帖子
        id=post.author.id
        recent_post=PostModel.query.filter(PostModel.author_id==id).limit(10)   #获取该帖子主人最近发表的10篇文章
        if post:
            content={
                'post':post,
                'recent_post':recent_post
            }
            return render_template('front/front_pdetial.html',**content)
        else:
            return abort(404)
    else:
        return abort(404)





@bp.route('/acommen/',methods=['POST',])                                #添加评论
@request_login
def acommen():
    '''
    :param: 评论内容（content），评论文章(id)
    :return: code 200  成功  json     评论成功
             code 403  失败  json     接受字段有问题
    '''
    if request.method=='POST':
        form=Acommen_verify(request.form)                               #获取评论文章id和评论内容
        if form.validate():                                             #判断用户传送的格式是否合法
            content=form.content.data
            author=g.front_user
            id=form.post_id.data
            post=PostModel.query.filter_by(id=id).first()               #获取这篇帖子
            commen=Commen_Model(content=content)                        #创建这条评论
            commen.post=post                                            #设置评论的帖子是那一条
            commen.author=author                                        #当前用户为评论的作者
            db.session.add(commen)
            db.session.commit()
            return  jsonify({'code':200,'message':'评论成功'})            #评论成功
        else:
            message=form.errors.popitem()[0][1]
            return jsonify({'code':403,'message':message})              #弹出第一条验证出错信息
    else:
        return  abort(404)


@bp.route('/commenLike/',methods=['POST'])                             #评论点赞
@request_login                                                         #登录装饰器
def commenLike():
    commen_id=request.form.get('commen_id')
    commen=Commen_Model.query.get(commen_id)
    if commen_id:
        user_id=g.front_user.id
        like=LikeModel.query.filter(LikeModel.user_id==user_id,LikeModel.commen_id==commen_id).first()

        if like and like.statue:
            return jsonify({'code':300,'message':'您已经点过赞了'})
        like=LikeModel(statue=True)
        like.user=g.front_user
        like.commen=commen
        db.session.add(like)
        db.session.commit()
        return jsonify({'code':200,'message':'点赞成功'})
    else:
        return jsonify({'code':404,'message':'找不到该帖子'})

@bp.route('/search/',methods=['GET'])                                 #搜索功能
def search():
    '''
    :param: 搜索内容(?contend=)
    :return: 搜索到的数据 list
    '''
    content=request.args.get('content')                              #获取搜索内容
    if content:                                                      #如果有内容
        content=str(content)
        content2='%'+content+'%'
        posts=PostModel.query.filter(PostModel.title.like(content2)).all()
        contents={
            'posts':posts,
            "content":content
        }
        return render_template('front/front_search.html',**contents)
    else:
        return abort(404)                                                 #跳转到自定义错误界面



@bp.route('/personal/',methods=['GET','POST'])                                  #个人中心
def personal():
    if request.method=='GET':
        user_id=request.args.get('user-id')
        if user_id:
            user=Front_user.query.filter_by(id=id).first()
            posts = PostModel.query.filter_by(author_id=user_id).slice(0, 8)  # 获取帖子从起始位置到结束位置的帖子阶段的帖子
            content = {
                'user': user,
                'posts': posts,
                'user_type': '1'  # 用于判别是用户访问还是自己访问
            }
            return render_template('front/front_personal.html', **content)

        else:
            user=g.front_user                                                   #当前用户
            posts = PostModel.query.filter_by(author_id=user.id).all()  # 获取帖子从起始位置到结束位置的帖子阶段的帖子
            content={
                'user':user,
                'posts':posts,
                'user_type':'1'                                                 #用于判别是用户访问还是自己访问
            }
            return render_template('front/front_personal.html',**content)
