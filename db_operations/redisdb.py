from time import time
import redis
from db_operations.dbOperations import DBOperations

class RedisDB(DBOperations):
    def __init__(self):
        self.redisdb = redis.Redis(host='localhost', port=6379, db=0)
        self.redisdb.set("visitorCount", 0)
        self.redisdb.delete("timestamp_counter")

    def getVisitorCount(self):
        current_val = self.redisdb.get("visitorCount").decode("UTF-8")
        return current_val

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