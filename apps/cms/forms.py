from wtforms import Form,StringField,IntegerField
from wtforms.validators import Length,Email,InputRequired,EqualTo,ValidationError,Regexp
from apps.models import PostModel,Commen_Model
from .models import CMS_user
from utils.memcached import mc
from flask import g

class Cms_login_verify(Form):               #CMS登录验证
    email=StringField(validators=[InputRequired(message='请输入数据'),Email(message='邮箱格式不正确')])  #验证邮箱格式
    passwd=StringField(validators=[InputRequired(message="请输入密码"),Length(6,12,message='密码长度不够')])#密码长度必须为6到12位
    remember=IntegerField(validators=[])


class Cms_resetpwd_verify(Form):
    oldpasswd=StringField(validators=[Length(6,20,message='密码长度不够,请重新输入密码')])
    newpasswd=StringField(validators=[Length(6,20,message='密码长度不够,请重新输入密码')])
    renewpasswd=StringField(validators=[EqualTo("newpasswd",message='两次输入不相同')])


class Cms_resetemail_verify(Form):          #邮箱验证码格式验证
    email=StringField(validators=[Email(message='请输入正确的邮箱')])
    email_code=StringField(validators=[Length(4,4,message="请输入正确格式的验证码")])

    def validate_email_code(self,field):    #如果用户名和密码都满足
        code=mc.get(self.email.data)        #从memcached中取用户名为email值得这个数
        if not code or field.data!=code:    #判断用户输入的邮箱号和验证码是否和先前获取的存放在mecached里面的一样，判断是否取得到
            raise ValidationError('邮箱或者验证码错误')
    def validate_email(self,field):
        email=g.cms_user.email
        if field.data==email:               #如果用户输入的邮箱的邮件名称和原来的邮箱一样
            raise ValidationError('您的邮箱和原始邮箱不能同名')

class Add_banner_verify(Form):               #添加banner图验证
    name=StringField(validators=[InputRequired(message='请输入Banner名称')])
    img_url=StringField(validators=[InputRequired(message='请输入图片链接地址')])
    link_url=StringField(validators=[InputRequired(message='请输入图片跳转地址')])
    priority=IntegerField(validators=[InputRequired(message='请输入优先级')])

class Update_banner_verify(Add_banner_verify):#更新banner图验证
    id=IntegerField(validators=[InputRequired()])


class Add_boarder_verify(Form):                          #添加板块验证
    name=StringField(validators=[InputRequired(message='请输入板块名称')])
    img_url=StringField(validators=[InputRequired(message='请输入图片链接地址')])
    intr=StringField(validators=[InputRequired(message='请输入板块简介')])
    notice=StringField(validators=[InputRequired(message='请输入公告信息')])

class Update_boarder_verify(Add_boarder_verify):        #修改板块验证
    id=IntegerField(validators=[InputRequired(message='获取板块ID错误')])

class Agoodpost_verify(Form):                           #设置帖子为精品贴验证
    id=IntegerField(validators=[InputRequired(message='帖子不存在')])
    def validate_id(self,field):
        id=field.data
        post=PostModel.query.filter_by(id=id).first()  #查找数据库中是否有这篇帖子
        if not post:
            raise ValidationError(message='该帖子不存在')

class Delgoodpost_verify(Form):                         #取消设置帖子为精品贴验证
    id=IntegerField(validators=[InputRequired(message='帖子不存在')])
    def validate_id(self,field):
        id=field.data
        post=PostModel.query.filter_by(id=id).first()  #查找数据库中是否有这篇帖子
        if not post:
            raise ValidationError(message='该帖子不存在')

class Delpost_verify(Form):                           #删除帖子
    id=IntegerField(validators=[InputRequired(message='帖子不存在')])
    def validate_id(self,field):
        id=field.data
        post=PostModel.query.filter_by(id=id).first()  #查找数据库中是否有这篇帖子
        if not post:
            raise ValidationError(message='该帖子不存在')


class aCmsUser_Verify(Form):                            #创建cms_user验证
    username=StringField(validators=[Length(min=2,max=16,message='密码长度为2到16位')])
    password=StringField(validators=[Regexp('[a-z0-9]{6,16}',message='密码为6到16位，字母数字下下划线')])
    password1=StringField(validators=[EqualTo("password",message='2次密码不一致')])
    email=StringField(validators=[Email(message='邮箱格式不正确')])
    def validate_email(self,field):
        user=CMS_user.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError(message='邮箱已注册')


class setPermission_Verify(Form):                     #设置后天权限验证
    user_id=IntegerField(InputRequired(message='用户传参错误'))
    role_id=IntegerField(InputRequired(message='角色传参错误'))
    set=IntegerField(InputRequired(message='修改类型不能为空'))


class DelCommen_Verify(Form):                           #删除帖子
    id=IntegerField(validators=[InputRequired(message='传参错误')])
    def validate_id(self,field):
        id=field.data
        commen=Commen_Model.query.filter_by(id=id).first()  #查找数据库中是否有这篇帖子
        if not commen:
            raise ValidationError(message='该帖子不存在')
