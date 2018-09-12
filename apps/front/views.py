from flask import Blueprint,render_template,request
from flask_mail import Message
import random

from exts import mail
bp=Blueprint('front',__name__)
@bp.route('/')
def index():
    return 'hello'


@bp.route('/send/')#测试邮箱是否发送成功
def send():
    mes=random.randrange(1000,9999)
    message=Message('我是刘杨，测试项目',recipients=['3086573022@qq.com'],body='您的验证码是'+str(mes))
    mail.send(message)
    return '发送成功'


