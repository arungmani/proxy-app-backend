import redis
import os
import json

# Connect to Redis using the REDIS_URI environment variable
redis_uri = os.getenv("REDIS_URI")
client = redis.Redis.from_url(redis_uri)

# Test the connection
try:
    client.ping()
    print("Connected to Redis!")
except redis.ConnectionError:
    print("Failed to connect to Redis.")


async def setCache(key, data):
    if client:
        client.rpush(key, data)
    else:
        print("NOT CONNECTED TO REDIS")


async def getCache(key):
    return client.lrange(key, 0, -1)


async def deleteCache(key):
    return client.delete(key)



