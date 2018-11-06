from redis import Redis

cache=Redis(host='127.0.0.1',port=6379)
print(cache.get('liuyang'))