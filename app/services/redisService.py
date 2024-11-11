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
task = {"id": 1, "name": "Repair bike", "priority": "high", "due_date": "2024-11-15"}


# Serialize the object to JSON format
# task_json = json.dumps(task)
# print(task)
# res15 = client.rpush("bikes:repairs", task_json)
# client.delete("bikes:repairs")

# # print(res15)
res16=client.lrange("notifications_cb5b9ab9-dd41-4651-9589-d106bc814320",0,-1)
print(res16)
# print(value.decode("utf-8"))  # Output: Hello, Redis!

async def storeNotifcationInRedis(user_ids, data):
    print("THE USER IDS AND THE TASK INFO IS", user_ids, data)

    # Convert `data` dictionary to JSON string
    data = json.dumps(data)

    if client:
        for user_id in user_ids:
            print("THE USER ID IS", user_id)
            res = client.rpush(f"notifications_{user_id}", data)
            print("REDIS NOTIFICATION STORED SUCCESSFULLY FOR THE USER", res)
    else:
        print("Not connected to redis")