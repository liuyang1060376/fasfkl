from exts import db
from datetime import datetime


class BoardModel(db.Model):         # 板块模型(id,标题，图片地址，简介，创建时间)
    __tablename__='boardmodel'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    name=db.Column(db.String(20),nullable=False)
    img_url=db.Column(db.String(255),nullable=False)
    intr=db.Column(db.String(100),nullable=False)
    create_time=db.Column(db.DateTime,nullable=False,default=datetime.now())
    notice=db.Column(db.Text)


# Banner模型
class Banner_Model(db.Model):  #定义一个，用来存放轮播图的信息
    '''
    1.id
    2.图片链接地址
    3.跳转链接地址
    4.优先级
    5.创建时间'''
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    img_url=db.Column(db.String(255),nullable=False)
    link_url=db.Column(db.String(255),nullable=False)
    priority=db.Column(db.Integer,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now())
    name=db.Column(db.String(50),nullable=False)


# 评论表
class Commen_Model(db.Model):
    __tablename__='commen'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)                                           #评论内容
    create_time=db.Column(db.DateTime,nullable=False,default=datetime.now())            #评论时间
    article_id=db.Column(db.Integer,db.ForeignKey('postmodel.id'),nullable=False)       #评论的文章id
    author_id=db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)   #评论作者

    author=db.relationship('Front_user',backref='commens')
    post=db.relationship('PostModel',backref='commens')


 #帖子模型
class PostModel(db.Model):
    __tablename__ = 'postmodel'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)                  #id
    title = db.Column(db.String(200),nullable=False)                                #标题
    content = db.Column(db.Text,nullable=False)                                     #内容
    isgood=db.Column(db.DateTime,nullable=True)                                     #加精
    create_time = db.Column(db.DateTime,default=datetime.now)                       #创建时间
    board_id = db.Column(db.Integer,db.ForeignKey("boardmodel.id"))                 #所属板块
    author_id = db.Column(db.String(100),db.ForeignKey("front_user.id"),nullable=False)#作者ID

    board = db.relationship("BoardModel",backref="posts")
    author = db.relationship("Front_user",backref='posts')

#点赞模型
class LikeModel(db.Model):
    __tablename__='like'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)#点赞人
    commen_id=db.Column(db.Integer,db.ForeignKey('commen.id'),nullable=False)      #点赞id
    statue=db.Column(db.Boolean,default=False,nullable=False)                      #是否已赞

    commen=db.relationship('Commen_Model',backref='likes')                         #对应的评论
    user=db.relationship('Front_user',backref='likes')


# #关注模型
class FollowModel(db.Model):
    __tablename__='Follow'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)     #关注人的id
    follow_id=db.Column(db.String(100),db.ForeignKey('boardmodel.id'),nullable=False)   #被关注人的id
    statue=db.Column(db.Boolean,default=False,nullable=False)







