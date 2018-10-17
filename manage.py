# -*- coding: UTF-8 -*-
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from exts import db
from app import app
from apps.models import PostModel
from apps.cms.models import CMS_user,CMS_role,cms_user_role,Permission
from apps.front.models import Front_user
from apps.models import Banner_Model,BoardModel,LikeModel,PostModel,Commen_Model


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

@manager.command                    #测试用户是否有游客权限
def has_permissio():
    user=CMS_user.query.first()
    result=user.has_permission(permissions=1)
    if result:
        print('成功')
    else:
        print('失败')


@manager.command            #创建500帖子模型
def create_post():
    for i in range(500):
        title='百度公司'+str(i)
        content='为了让更多开发者学习百度UNIT对话系统开发技能，8月30日起每周四14：00-15:30，百度与InfoQ联合推出了“ 从入门到实战 百度UNIT对话系统开发训练营”主题活动，百度的三位大咖级专家联合出席讲授三门线上课程，从UNIT对话系统的基本结构和功能入手，介绍UNIT核心模块和常用技术，以及UNIT平台底层机制，零起步零编程，教你快速完成对话系统的搭建和应用，掌握UNIT高级实用技巧，完成对话系统全套开发实践。'
        board=BoardModel.query.first()
        author=Front_user.query.first()
        post=PostModel(title=title,content=content)
        post.board=board
        post.author=author
        db.session.add(post)
        db.session.commit()
    print('创建成功')


@manager.option('-u','--username',dest='username')                    #创建一个前台用户
@manager.option('-p','--passwd',dest='passwd')
@manager.option('-t','--telephone',dest='telephone')
def create_front(username,passwd,telephone):
    user=Front_user(username=username,passwd=passwd,telephone=telephone)
    db.session.add(user)
    db.session.commit()
    print('创建前台用户成功')




if __name__ == '__main__':
    manager.run()

