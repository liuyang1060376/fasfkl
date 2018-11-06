from flask import Blueprint,request,jsonify, make_response,g
from flask_mail import Message
from exts import mail
from utils.miaodi.miaodi_sms_regist import sendRegistMessage
from random import randrange
from utils.captcha import ValidCodeImg
from io import BytesIO
from .forms import mobile_verify,resetpasswd_verify
from apps.front.decorators import request_login
from utils.memcached import mc
import qiniu
bp=Blueprint('common',__name__,url_prefix='/common')
@bp.route('/')
def index():
    return 'common'


'''错误代码500；服务器异常  200 成功   错误代码400： 没有输入邮箱账号'''
@bp.route('/send_email_code/',methods=['GET'])                                          #发送邮箱验证码验证
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




'''200：发送成功，
code 403(表单验证失败,返回具体验证信息)
code 404(未输入)
'''
@bp.route('/send_message/',methods=['GET','POST'])          #发送注册短信验证码
def send_message():
    '''
    :param:mobile
    :return:
    '''
    if request.method=='POST':
        form=mobile_verify(request.form)
        if form.validate():
            code = randrange(1000, 9999)
            code=str(code)
            mobile=form.mobile.data
            smsContent = '【飞讯社区】您的验证码为{0}，请于5分钟内正确输入，如非本人操作，请忽略此短信。'.format(code)
            sendRegistMessage(mobile, smsContent)
            mc.set(mobile,code,300)    #把验证码存放在memcached里面,过期时间为5分钟
            print('{0}的验证码为{1}'.format(mobile,code))
            return  jsonify({'code':200,'message':'发送成功'})
        else:
            message=form.errors.popitem()[1][0]
            return jsonify({'code':403,'message':message})









@bp.route('/refreshcode/')        #刷新验证码
def refreshcode():
    imgcode=ValidCodeImg()
    data,valid_str=imgcode.getValidCodeImg()   #获取随机生成的图片和验证码
    out=BytesIO()       #创建一个ByteIo对象
    out.write(data) #把图片保存到out中
    out.seek(0)   #把光标指向最开始
    resp=make_response(out.read())   #把图片从Byteio中读出来
    resp.content_type='image/png'    #设置图片的格式
    valid_str=valid_str.lower()
    mc.set(valid_str,valid_str.lower(),time=300)     #把图形验证码存放在Mecached里面，设置图形验证码的过期时间为5分钟
    return resp


@bp.route('/uptoken/')         #qiniu云官方提供的接口
def uptoken():
    access_key = 'H23yW6b9whf42VT-eCaTxc4mHeRrOIhPtTbA1KNX'
    secret_key = 'teaFq7bSuo7oq3Sh_zy8aJR80H1xk0CPmJ8N3net'
    q = qiniu.Auth(access_key,secret_key)
    bucket = 'boards'
    token = q.upload_token(bucket)
    return jsonify({"uptoken":token})











