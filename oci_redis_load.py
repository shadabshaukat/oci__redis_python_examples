import redis
import logging
import random
import string

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Connect to Redis
redis_client = redis.StrictRedis(
    host='*****.ap-mumbai-1.oci.oraclecloud.com',
    charset='utf-8',
    ssl=True,
    decode_responses=True,
    port=6379
)
redis_client_replica = redis.StrictRedis(host='***.ap-mumbai-1.oci.oraclecloud.com', charset='utf-8', ssl=True, decode_responses=True, port=6379)

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

# Generate and write 100 random records
logging.info("Generating and writing 100 random records to Redis")
keys = []
for i in range(100):
    key = f"key_{i}"
    value = random_string(10)
    keys.append(key)
    redis_client.set(key, value)

# Read the values for the keys
logging.info("Reading 100 records from Redis")
for key in keys:
    value = redis_client_replica.get(key)
    if value is not None:
        print(f"Value for {key}: {value}")
    else:
        print(f"Key {key} not found")
