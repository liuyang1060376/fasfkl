from datetime import datetime
import time
def a():
    a='2018-11-04'
    time1=datetime.strptime(a,"%Y-%m-%d")
    time2=datetime.now()
    print(type(time1))
    print(type(time2))
    time=(time2-time1).total_seconds()
    if time < 60:
        return '刚刚发布'
    elif time > 60 and time < 60 * 60:
        sj = int(time / 60)
        return '{0}分钟前发布'.format(sj)
    elif time > 60 * 60 and time < 60 * 60 * 24:
        sj = int(time / (60 * 60))
        print(sj)
        return '{0}小时前发布'.format(sj)
    elif time > 60 * 60 * 24 and time < 60 * 60 * 24 * 3:
        sj = int(time / 60 * 60 * 24)
        return '{0}天前发布'.format(sj)

if __name__ == '__main__':
    print(a())