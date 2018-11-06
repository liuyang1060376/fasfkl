from flask import Flask
from exts import db,mail
from flask_wtf import CSRFProtect
import config
import math
from apps.cms.views import bp as cms_bp     #导入后台蓝图
from apps.common.views import bp as common_bp  #导入公共蓝图
from apps.front.views import bp as front_bp    #导入前台蓝图
from ueditor import bp as ueditor           #导入一个编辑器
from datetime import datetime



app = Flask(__name__)               #初始化程序
CSRFProtect(app)                    #把app添加到CSRFProtect中
app.register_blueprint(front_bp)    #导入前台蓝图
app.register_blueprint(common_bp)   #导入公共模块蓝图
app.register_blueprint(cms_bp)      #导入后台模块蓝图
app.register_blueprint(ueditor)     #导入一个编辑器蓝图文件
app.config.from_object(config)   #导入配置文件
db.init_app(app)                 #把db和app绑定在一起，使其获得config里面关于数据库的配置信息
mail.init_app(app)               #把mail和app绑定在一起，使其获得config里面关于邮箱的的配置信息


# 自定义时间模板过滤器
@app.template_filter('settime')
def settim(value):
    if isinstance(value,datetime):
        now=datetime.now()
        time=(now-value).total_seconds()
        if time<60:                                 #小于60秒
            return '刚刚发布'
        elif time>60 and time<60*60:                #大于60秒小于60分钟
            sj=int(time/60)
            return '{0}分钟前发布'.format(sj)
        elif time>60*60 and time <60*60*24:         #24小时前
            sj=int(time/(60*60))
            return '{0}小时前发布'.format(sj)
        elif time>60*60*24 and time<60*60*24*3:     #3天前
            sj=int(time/(60*60*24))
            return '{0}天前发布'.format(sj)
    else:
        return value

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000)                       #如果这个程序做为主文件运行，则运行app.run()

