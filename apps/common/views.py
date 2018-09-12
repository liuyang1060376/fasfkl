from flask import Blueprint,request,jsonify,g
from flask_mail import Message
from exts import mail
from random import randrange
from utils.memcached import mc
bp=Blueprint('common',__name__,url_prefix='/common')
@bp.route('/')
def index():
    return 'common'


'''错误代码500；服务器异常  200 成功   错误代码400： 没有输入邮箱账号'''
@bp.route('/send_email_code/')                                  #发送邮箱验证码验证
def send_email_code():
    email=request.args.get('email')     #获取get方式发送过来的email
    if not email:           #如果没有输入email
        return jsonify({'code':400,'message':'请输入您的邮箱账号'})
    code = randrange(1000, 9999)    #生成一个随机的四位数的验证码
    code=str(code)
    message=Message('网络邮箱验证',recipients=[email],body='您正在修改您的默认邮箱：验证码为'+code+',验证码的有效时间是10分钟。[小杨科技]') #编辑短信内容
    try:
        mail.send(message)     #发送信息
        print(message)       #打印一下验证码，方便调试
        mc.set(email,code,time=600)          #把邮箱和验证码绑定在一起存放在memcached里面，过期时间是10分钟
        return jsonify({'code': 200, 'message': '发送成功'})
    except:
        return jsonify({'code':500,'message':'网络异常' })


