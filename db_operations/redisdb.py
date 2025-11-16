from time import time
import redis
from db_operations.dbOperations import DBOperations
import os

class RedisDB(DBOperations):
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redisdb = redis.Redis(host=redis_host, port=redis_port, db=0)
        #self.redisdb.set("visitorCount", 0)
        self.redisdb.delete("timestamp_counter")

    def getVisitorCount(self):
        current_val = self.redisdb.get("visitorCount").decode("UTF-8")
        return int(current_val)

    def clearVisitorCount(self):
        self.redisdb.set("visitorCount", 0)
        return 

    def incrementVisitorCountandReturn(self):
       self.redisdb.incr("visitorCount")
       current_val = self.getVisitorCount() 
       return current_val


    def logVisitTimestamp(self):
        unix_time = int(time())
        self.redisdb.hincrby("timestamp_counter", unix_time, 1)
        return

    def fetchAllTimestamps(self):
        data = self.redisdb.hgetall("timestamp_counter")
        decoded = [(int(x), int(data[x])) for x in data]
        return decoded