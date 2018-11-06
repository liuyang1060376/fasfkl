from exts import db
from datetime import datetime


class BoardModel(db.Model):         # 板块模型(id,标题，图片地址，简介，创建时间)
    __tablename__='boardmodel'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    like_number=db.Column(db.Integer,default=0)
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
    like_number=db.Column(db.Integer,default=0)                                     #点赞数量
    content = db.Column(db.Text,nullable=False)                                     #内容
    browse=db.Column(db.Integer,nullable=True)
    isgood=db.Column(db.DateTime,nullable=True)                                     #加精
    create_time = db.Column(db.DateTime,default=datetime.now)                       #创建时间
    board_id = db.Column(db.Integer,db.ForeignKey("boardmodel.id"))                 #所属板块
    author_id = db.Column(db.String(100),db.ForeignKey("front_user.id"),nullable=False)#作者ID

    board = db.relationship("BoardModel",backref="posts")
    author = db.relationship("Front_user",backref='posts')

#评论点赞模型
class LikeModel(db.Model):
    __tablename__='like'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)#点赞人
    commen_id=db.Column(db.Integer,db.ForeignKey('commen.id'),nullable=False)      #评论的id
    statue=db.Column(db.Boolean,default=False,nullable=False)                      #是否已赞

    commen=db.relationship('Commen_Model',backref='likes')                         #对应的评论
    user=db.relationship('Front_user',backref='likes' )


#帖子点赞模型
class PostLikeModel(db.Model):
    __tablename__='post_like'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False) #点赞人
    post_id=db.Column(db.Integer,db.ForeignKey('postmodel.id'),nullable=False)           #帖子id
    statue=db.Column(db.Boolean,default=False,nullable=False)                       #是否已赞

    post=db.relationship('PostModel',backref='likes')
    user=db.relationship('Front_user',backref='post_likes')

# #关注板块模型
class FollowModel(db.Model):
    __tablename__='follow_board'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    board_id=db.Column(db.Integer,db.ForeignKey('boardmodel.id'))         #板块id
    user_id=db.Column(db.String(100),db.ForeignKey('front_user.id'))      #关注人的id
    statue=db.Column(db.Boolean,default=True)                             #关注状态

    user=db.relationship('Front_user',backref='fboard' )
    board=db.relationship('BoardModel',backref='users')
# 点赞用户模型
class likeUserModel(db.Model):
    __tablename__='like_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('front_user.id'))    # 被dian'zan
    user_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))  # 关注人的id
    statue = db.Column(db.Boolean, default=True)  # 关注状态












