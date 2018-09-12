host='127.0.0.1'
username='root'
passwd='12345678'
db='zlkt'
port=3306
DB_URI='mysql+pymysql://{username}:{passwd}@{host}:{port}/{db}?charset=utf8' \
       ''.format(username=username,passwd=passwd,host=host,port=port,db=db)
SQLALCHEMY_DATABASE_URI=DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=False
import os
SECRET_KEY=os.urandom(24)     #加盐
# PERMANENT_SESSION_LIFETIME=300 #设置sessionc持久化的存活时间
CMS_USER_ID='FDFF'    #定义一个用来存放session的变量
'''配置邮箱链接内容'''
MAIL_SERVER='smtp.qq.com'    #邮箱发送服务器地址
MAIL_PORT=587                #端口号
MAIL_USE_TLS=True
MAIL_USERNAME='1060376291@qq.com'
MAIL_PASSWORD='vaalbbytmynqbeeh'   #授权码
MAIL_DEFAULT_SENDER='1060376291@qq.com'
