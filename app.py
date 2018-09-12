from flask import Flask,url_for
from exts import db,mail
from flask_wtf import CSRFProtect
import config
from apps.cms.views import bp as cms_bp     #导入后台蓝图
from apps.common.views import bp as common_bp  #导入公共蓝图
from apps.front.views import bp as front_bp    #导入前台蓝图

app = Flask(__name__)               #初始化程序
CSRFProtect(app)                    #把app添加到CSRFProtect中
app.register_blueprint(front_bp)    #导入前台蓝图
app.register_blueprint(common_bp)   #导入公共模块蓝图
app.register_blueprint(cms_bp)      #导入后台模块蓝图
app.config.from_object(config)   #导入配置文件
db.init_app(app)                 #把db和app绑定在一起，使其获得config里面关于数据库的配置信息
mail.init_app(app)               #把mail和app绑定在一起，使其获得config里面关于邮箱的的配置信息




if __name__ == '__main__':
    app.run(debug=True)                       #如果这个程序做为主文件运行，则运行app.run()
