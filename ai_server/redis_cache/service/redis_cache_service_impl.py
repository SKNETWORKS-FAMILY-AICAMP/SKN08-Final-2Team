# redis_cache_service_impl.py

import redis
import os
from dotenv import load_dotenv

# .env 파일 로딩
load_dotenv()

class RedisCacheServiceImpl:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.redisClient = redis.StrictRedis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                password=os.getenv("REDIS_PASSWORD", None),
                decode_responses=True
            )
        return cls.__instance
    
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def storeKeyValue(self, key, value):
        try:
            self.redisClient.set(key, value)
        except Exception as e:
            print('Error storing access token in Redis:', e)
            raise e

    def getValueByKey(self, key):
        try:
            return self.redisClient.get(key)
        except Exception as e:
            print("redis key로 value 찾는 중 에러 발생:", e)
            raise e

    def deleteKey(self, key):
        try:
            result = self.redisClient.delete(key)
            if result == 1:
                print(f"유저 토큰 삭제 성공: {key}")
                return True
            return False
        except Exception as e:
            print("redis key 삭제 중 에러 발생:", e)
            raise e
