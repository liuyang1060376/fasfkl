from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class Permission(object):     #权限模型
    #1. 255用二进制表示为11111111，表示最高权限
    ALL_PERMISSION= 0b11111111
    #2. 访客权限
    VISITOR=        0b00000001
    #3.  管理帖子
    POSTER=         0b00000010
    #4.  管理评论的权限
    COMMENTER=      0b00000100
    #5.  管理板块的权限
    BOARDER=        0b00001000
    #6.   管理前台用户的权限
    FRONTUSER=      0b00010000



# 创建cmsuser和cms_role的中间表
cms_user_role=db.Table('cms_user_role',
                       db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
                       db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
                       )

class CMS_role(db.Model):                   #角色表
    __tablename__='cms_role'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(20),nullable=False)            #名称
    desc=db.Column(db.String(255),nullable=False)           #简介
    role_permission=db.Column(db.Integer,default=Permission.VISITOR)    #角色权限
    create_time=db.Column(db.DateTime,default=datetime.now())           #建立时间

    users=db.relationship('CMS_user',secondary=cms_user_role,backref='roles')    #和CMS表建立多对多的关系

class CMS_user(db.Model):     #创建一个CMS用户类（用户名，密码，email,连接时间）
    __tablename__='cms_user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),nullable=False)
    _passwd=db.Column(db.String(255),nullable=False)       #密码这种字段必须在数据库中是加密的，这样能防止黑客进攻，密码泄露
    email=db.Column(db.String(20),nullable=False,unique=True)
    join_time=db.Column(db.DateTime,nullable=False,default=datetime.now())
    def __init__(self,username,passwd,email):           #重写了类初始变量，使其直接输入的时候通过passwd可以修改私有变量_passwd
        self.username=username
        self.passwd=passwd
        self.email=email


    @property
    def passwd(self):
        return self._passwd
    @passwd.setter      #对存放数据库的密码进行加密
    def passwd(self,raw_passwd):
        self._passwd=generate_password_hash(raw_passwd)

    def check_password(self,raw_passwd):
        result=check_password_hash(self.passwd,raw_passwd)#对输入的密码和数据库密码进行对比
        return result

    @property                                                   #获取该用户的所有权限
    def permission(self):
        all_permission=0
        if  not(self.roles):                                    #如果这个用户角色
            return 0
        else:
            for role in self.roles:                             #遍历里面的角色
                all_permission|=role.role_permission            #把里面角色进行或运算
            return  all_permission                              #得到最高权限返回


    def has_permission(self,permissions):                        #查看用户是否有某个权限
        return (self.permission & permissions) ==permissions
        #把用户的权限和需要的权限对比，如果返回的和他本身相等，则用户有这个权限



