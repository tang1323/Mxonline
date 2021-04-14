
import redis

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf8", decode_responses=True)

r.set("mobile", "123")
# print(r.get("mobile"))
# 这个是过期，让这个mobile一秒钟后过期
r.expire("mobile", 1)
import time
time.sleep(1)
print(r.get("mobile"))



