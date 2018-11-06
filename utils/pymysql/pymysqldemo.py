


import pymysql.cursors

# 连接数据库
connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='12345678',
    db='forum',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()

