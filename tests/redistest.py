import redis
from random import randint

r = redis.Redis(host='localhost', port=6379, db=0)
r.set("visitorCount", 0)

for i in range(1000):
    for j in range(randint(1, 1000)):
        r.incr('visitorCount')
    value = r.get('visitorCount').decode("UTF-8")
    print(value)

r.close()
