'''专门用来存放一些短信验证码，一些不重要，无需长期保存的数据'''
import memcache
mc=memcache.Client(['127.0.0.1:11211'])
