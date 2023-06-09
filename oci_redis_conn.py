import redis
import logging

logging.basicConfig(level=logging.DEBUG)

# Connect to Redis
redis_client = redis.StrictRedis(host='****.ap-mumbai-1.oci.oraclecloud.com', charset='utf-8', ssl=True, decode_responses=True, port=6379)
redis_client_replica = redis.StrictRedis(host='*****.redis.ap-mumbai-1.oci.oraclecloud.com', charset='utf-8', ssl=True, decode_responses=True, port=6379)

# Set a key-value pair
redis_client.set("my_key", "Hello, Redis!")

# Run a GET command
key = "my_key"
value = redis_client_replica.get(key)
if value is not None:
    print(f"Value for {key}: {value}")
else:
    print(f"Key {key} not found")
