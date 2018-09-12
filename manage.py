# -*- coding: UTF-8 -*-
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from exts import db
from app import app
from apps.cms.models import CMS_user,CMS_role,cms_user_role,Permission
manager=Manager(app)    #创建一个manager对象

Migrate(app,db)     #把db和app绑定在一起
manager.add_command('db',MigrateCommand)   #使MigrateCommand下的子命令全部添加到manager下，名称为db

@manager.option('-u','--username',dest='username')
@manager.option('-p','--passwd',dest='passwd')
@manager.option('-e','--email',dest='email')
def create_cmsuser(username,passwd,email):             #自定义一个创建CMSuser的命令
    user=CMS_user(username=username,passwd=passwd,email=email)
    db.session.add(user)
    db.session.commit()
    print('创建用户成功')

@manager.option('-u','--username',dest='username')
def delete_cmsuser(username):                           #自定义一个删除CMSuser的命令
    db.session.delete(CMS_user.query.filter_by(username=username).first())
    db.session.commit()
    print('删除成功')

@manager.command            #创建角色
def create_role():
    role1=CMS_role(name='游客',desc='只可以对网站进行访问，没有任何权限',role_permission=Permission.VISITOR)
    role2=CMS_role(name='经营者',desc='可以管理评论,帖子，前台用户,访问网站',role_permission=Permission.FRONTUSER|Permission.VISITOR|Permission.POSTER|Permission.COMMENTER)
    role3=CMS_role(name='管理员',desc='拥有本系统所有功能')
    role3.role_permission=Permission.COMMENTER|Permission.POSTER|Permission.VISITOR|Permission.FRONTUSER|Permission.BOARDER|Permission.CMSUSER
    role4=CMS_role(name='开发者',desc='对系统进行修改的最高权限',role_permission=Permission.ALL_PERMISSION)
    db.session.add_all([role1,role2,role3,role4])
    db.session.commit()
    print('创建成功角色')


@manager.option('-u','--username',dest='username')      #把用户添加到某个角色中
@manager.option('-n','--name',dest='name')
def add_user_to_role(username,name):
    user=CMS_user.query.filter_by(username=username).first()
    if user:
        role=CMS_role.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('添加到角色成功')
        else:
            print('角色不存在')
    else:
        print('不存在这个用户')


if __name__ == '__main__':
    manager.run()

