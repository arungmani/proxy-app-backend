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


# async def getNotifications(user_id):
#     notifications = client.lrange(f"notifications_{user_id}", 0, -1)
#     decoded_notifications = [
#         json.loads(notification.decode("utf-8")) for notification in notifications
#     ]
#     return decoded_notifications


# async def deleteNotification(user_id):
#     return client.delete(f"notifications_{user_id}")


# async def storeNotifcationInRedis(user_ids, data):
#     print("THE USER IDS AND THE TASK INFO IS", user_ids, data)

#     # Convert `data` dictionary to JSON string
#     data = json.dumps(data)
#     if client:
#         for user_id in user_ids:
#             res = client.rpush(f"notifications_{user_id}", data)
#             print("REDIS NOTIFICATION STORED SUCCESSFULLY FOR THE USER", res)
#     else:
#         print("Not connected to redis")
