from logging.handlers import RotatingFileHandler

from flask import Flask,render_template
from exts import db,mail
from flask_wtf import CSRFProtect
import config
import logging
from apps.cms.views import bp as cms_bp     #导入后台蓝图
from apps.common.views import bp as common_bp  #导入公共蓝图
from apps.front.views import bp as front_bp    #导入前台蓝图
from ueditor import bp as ueditor           #导入一个编辑器



app = Flask(__name__)               #初始化程序
CSRFProtect(app)                    #把app添加到CSRFProtect中
app.register_blueprint(front_bp)    #导入前台蓝图
app.register_blueprint(common_bp)   #导入公共模块蓝图
app.register_blueprint(cms_bp)      #导入后台模块蓝图
app.register_blueprint(ueditor)     #导入一个编辑器蓝图文件
app.config.from_object(config)   #导入配置文件
db.init_app(app)                 #把db和app绑定在一起，使其获得config里面关于数据库的配置信息
mail.init_app(app)               #把mail和app绑定在一起，使其获得config里面关于邮箱的的配置信息

# # 配置日志信息
# # 设置日志的记录等级
# logging.basicConfig(level=logging.INFO)
# # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
# file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
# formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# # 为刚创建的日志记录器设置日志记录格式
# file_log_handler.setFormatter(formatter)
# # 为全局的日志工具对象（flask app使用的）添加日记录器
# logging.getLogger().addHandler(file_log_handler)

@app.route('/test/')
def test():
    return render_template('front/front_search.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')                       #如果这个程序做为主文件运行，则运行app.run()

