from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
import enum
class GenderEnum(enum.Enum):   #构造了个性别枚举类
    man=1
    woman=2
    secret=3
    unknow=4

class Front_user(db.Model):     #创建一个前台用户类
    __tablename__='front_user'  #表明
    id=db.Column(db.String(200),primary_key=True,default=shortuuid.uuid)    #用户id
    username=db.Column(db.String(20),nullable=False)                        #用户名
    telephone=db.Column(db.String(11),nullable=False,unique=True)           #手机号
    __passwd=db.Column(db.String(200),nullable=False)                        #密码
    avatar=db.Column(db.String(200))                                        #头像
    realname=db.Column(db.String(20))                                       #真实姓名
    personal_introduction=db.Column(db.String(150))                         #个人介绍
    gender=db.Column(db.Enum(GenderEnum),default=GenderEnum.unknow)         #性别
    join_time=db.Column(db.DateTime,default=datetime.now())                 #链接时间
    is_delete=db.Column(db.Boolean,default=False,nullable=False)            #用于加入黑名单

    def __init__(self,*args,**kwargs):
        if 'passwd' in kwargs:      #对接受过来的密码进行一段处理
            passwd=kwargs.get('passwd')
            self.passwd=passwd
            kwargs.pop('passwd')  #删除这个passwd
        super(Front_user, self).__init__(*args,**kwargs)    #剩下的内容交个父类处理



    @property           #对密码进行加密
    def passwd(self):
        return self.__passwd
    @passwd.setter
    def passwd(self,passwd):
        self.__passwd=generate_password_hash(passwd)

    def check_passwd(self,passwd):          #查看用户输入的密码是否正确
        return check_password_hash(self.passwd,passwd)




