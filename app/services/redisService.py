import redis

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, protocol=3)

# Test the connection
try:

    if redis_client:
        print("Connected to Redis!")
except redis.ConnectionError:
    print("Failed to connect to Redis.")

redis_client.set("my_key", "Hello, Redis!")

# Get the value for a key
# value = redis_client.get("my_key")
# print(value.decode("utf-8"))  # Output: Hello, Redis!