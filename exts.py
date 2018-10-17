from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
db=SQLAlchemy()                 #建立数据库链接

mail=Mail()                      #创建一个邮箱链接的对象
