from wtforms import Form,StringField,IntegerField,ValidationError
from wtforms.validators import Regexp, EqualTo, Length,InputRequired
from utils.memcached import mc
from .models import Front_user
from apps.models import PostModel
from flask import g

class Regist_verify(Form):              #注册表单验证
    ''' 用户名长度为2到20位
        密码要求最少6位最大20位，只能是数字字母下划线
        手机号码满足标准格式，且不能和数据库重复
        验证码格式4位，和memcache的验证码一致
        图片验证码要求4位，不区分大小写，和memcached的验证码一致
    '''
    username=StringField(validators=[Regexp(r'.{2,20}',message='用户名输入不正确')])
    passwd=StringField(validators=[Regexp(r"\w{6,20}",message='密码输入格式不正确')])
    repasswd=StringField(validators=[EqualTo('passwd',message='两次密码输入不一致')])
    mobile=StringField(validators=[Regexp(r'1[34578]\d{9}',message='手机号码输入错误')])
    verifycode=StringField(validators=[Regexp(r'\d{4}',message='验证码输入错误')])
    imgverifycode=StringField(validators=[Regexp(r"\w{4}",message='验证码最多4位')])
    '''自定义手机验证码验证'''
    def validate_mobile(self,field):
        mobile=field.data
        user=Front_user.query.filter_by(telephone=mobile).first()
        if user:
            raise  ValidationError(message='您已注册，请勿重新注册')
    '''自定义短信验证码验证'''
    def validate_verifycode(self,field):
        mobile=self.mobile.data
        code=mc.get(mobile)             #从memcached中取出这个手机号码对应的验证码
        print(code)
        print(type(code))
        if not code or code!=field.data:
            raise ValidationError(message='手机验证码错误')
    '''自定义图片验证码验证'''
    def validate_imgverifycode(self,field):
        data=field.data.lower()
        code=mc.get(data)   #从图片中取出验证码
        if not code or code!=data:
            raise ValidationError('图片验证码错误')




class Login_verify(Form):                                                   # 登录验证
    mobile=StringField(validators=[Regexp(r'1[3578]\d{9}',message='手机号码输入错误')])
    passwd=StringField(validators=[Regexp(r'.{6,20}')])

    def validate_mobile(self,field):
        mobile=field.data
        passwd=self.passwd.data
        user=Front_user.query.filter_by(telephone=mobile).first()
        if not user:
            raise ValidationError('没有这个用户，请注册')
        if not user.check_passwd(passwd):
            raise ValidationError('用户密码错误')

class Post_verify(Form):                                                     #用户发帖验证
    title=StringField(validators=[InputRequired(message='请输入标题')])
    content=StringField(validators=[InputRequired(message='请输入文章内容')])
    id=IntegerField(validators=[InputRequired(message='请选择板块')])
    img_code=StringField(validators=[Regexp(r'\w{4}',message='验证码格式不正确')])
    def validate_img_code(self,field):
        img_code=field.data.lower()
        code=mc.get(img_code)
        if not code or code!=img_code:
            raise ValidationError('验证码不正确')


class Acommen_verify(Form):                                                 #添加评论验证
    post_id=IntegerField(validators=[InputRequired(message='你评论的帖子不存在')])
    content=StringField(validators=[InputRequired(message='请输入评论内容哦！')])
    def validate_article_id(self,field):
        post=PostModel.query.filter_by(id=field.article_id).first
        if not post:
            raise ValidationError('您评论的帖子不存在哟')


class upUser_verify(Form):                                                  #修改用户基本信息
    username=StringField(validators=[Regexp(r'.{2,16}',message='用户名格式不正确')])
    avatar=StringField(validators=[InputRequired('请选择您的头像')])
    intr=StringField(validators=[InputRequired('简介信息不能为空哦')])



class resetpassword_Veriyf(Form):
    password = StringField(validators=[Regexp('[a-z0-9]{6,16}', message='密码为6到16位，字母数字下下划线')])
    password1 = StringField(validators=[EqualTo("password", message='2次密码不一致')])
    code = StringField(validators=[Regexp(r'\d{4}', message='验证码输入错误')])

    '''自定义短信验证码验证'''
    def validate_code(self, field):
        mobile =g.front_user.telephone
        code = mc.get(mobile)  # 从memcached中取出这个手机号码对应的验证码
        print(code)
        print(type(code))
        if not code or code != field.data:
            raise ValidationError(message='手机验证码错误')