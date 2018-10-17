'''数据库连接配置'''
host='127.0.0.1'
username='root'
passwd='12345678'
db='forum'
port=3306
DB_URI='mysql+pymysql://{username}:{passwd}@{host}:{port}/{db}?charset=utf8' \
       ''.format(username=username,passwd=passwd,host=host,port=port,db=db)
SQLALCHEMY_DATABASE_URI=DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=False


import os
# SECRET_KEY=os.urandom(24)     #加盐
SECRET_KEY='12321U3IOFKSAFHAKSFJKAFSAF'


'''session存放字段'''
# PERMANENT_SESSION_LIFETIME=300 #设置sessionc持久化的存活时间
CMS_USER_ID='FDFFfdsafafds'    #定义一个用来存放cms_user的session的变量
FRONT_USER_ID='FSDJFLSFJKLSKF' #定义一个用来存放front_user的session变量


'''配置邮箱链接内容'''
MAIL_SERVER='smtp.qq.com'    #邮箱发送服务器地址
MAIL_PORT=587                #端口号
MAIL_USE_TLS=True
MAIL_USERNAME='1060376291@qq.com'
MAIL_PASSWORD='vaalbbytmynqbeeh'   #授权码
MAIL_DEFAULT_SENDER='1060376291@qq.com'


# 七牛云相关服务
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "H23yW6b9whf42VT-eCaTxc4mHeRrOIhPtTbA1KNX"
UEDITOR_QINIU_SECRET_KEY = "teaFq7bSuo7oq3Sh_zy8aJR80H1xk0CPmJ8N3net"
UEDITOR_QINIU_BUCKET_NAME = "boards"            #上传到7牛云空间的名字
UEDITOR_QINIU_DOMAIN = "http://pfc2azd93.bkt.clouddn.com/"





