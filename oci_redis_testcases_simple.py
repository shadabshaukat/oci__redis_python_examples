"""
OCI Redis Performance and Functionality Testing for Real-World Applications

Test 1: Basic read and write operations
This test case checks the basic functionality of the Redis instance by setting and getting a key-value pair. It ensures that basic operations like writing and reading data are working correctly.

Test 2: Expiration
This test case sets a key-value pair with an expiration time. It verifies that the Redis instance can handle expiring keys and that it correctly removes the keys after the specified time.

Test 3: Increment
This test case increments the value of a key. It ensures that the Redis instance can perform atomic increment operations on numeric values, which is useful for applications that need to maintain counters.

Test 4: List data structure
This test case manipulates a Redis list by pushing and popping elements. It ensures that the Redis instance can handle list data structures, which are useful for maintaining queues, stacks, or other ordered collections of items.

Test 5: Set data structure
This test case manipulates a Redis set by adding and removing elements. It ensures that the Redis instance can handle set data structures, which are useful for maintaining collections of unique items.

Test 6: Hash data structure
This test case manipulates a Redis hash by setting and getting field-value pairs. It ensures that the Redis instance can handle hash data structures, which are useful for storing objects with multiple fields.

Test 7: Bulk insert and read
This test case inserts multiple key-value pairs in bulk and reads them back. It ensures that the Redis instance can handle a large number of operations efficiently and tests the replication capabilities of a Redis cluster.

Test 8: Redis Pipelining
This test case demonstrates the use of Redis pipelining to perform multiple operations more efficiently. It tests the performance improvement provided by pipelining in scenarios where there are many round-trip communications between the client and the Redis instance.

Test 9: Large data payload
This test case stores and retrieves a large JSON object. It ensures that the Redis instance can handle large data payloads, which is useful for applications that need to store complex data structures or large objects.

Test 10: Sorted sets for ranking
This test case manipulates a Redis sorted set to maintain a leaderboard of users and their scores. It ensures that the Redis instance can handle sorted sets and perform operations like ranking, which are useful for applications that need to maintain ordered collections of items with scores.

Test 11: Publish and Subscribe (Pub/Sub)
This test case demonstrates the use of Redis Pub/Sub to send messages between a publisher and a subscriber. It ensures that the Redis instance can handle publish and subscribe operations, which are useful for applications that need to communicate between multiple components in real-time.

Test 12: Transactions
This test case demonstrates the use of Redis transactions to perform multiple operations atomically. It ensures that the Redis instance can handle transactions, which are useful for applications that need to maintain consistency and perform multiple operations in a single unit of work.

Test 13: Geospatial indexes
This test case manipulates a Redis geospatial index to store the locations of cities and calculate the distance between them. It ensures that the Redis instance can handle geospatial operations, which are useful for applications that need to store and query location-based data.

Test 14: LUA Scripting
This test case uses a Lua script to perform a custom operation on a Redis key. It ensures that the Redis instance can execute Lua scripts, which allows applications to perform complex operations in a single round-trip to the Redis server.

Test 15: HyperLogLog
This test case demonstrates the use of Redis HyperLogLog to estimate the number of unique items in a large dataset. It ensures that the Redis instance can handle HyperLogLog data structures, which provide a memory-efficient way to count unique elements in large datasets, such as the number of unique visitors to a website.
"""


import redis
import time
import string
import random

# Replace these with your primary and replica endpoints
primary_host = "amaaaaaap77apcqandw5nv2266miqop6d3adkg3zbcwdpykfnqf24ge66t3a-p.redis.ap-mumbai-1.oci.oraclecloud.com"
primary_port = 6379
replica_host = "amaaaaaap77apcqandw5nv2266miqop6d3adkg3zbcwdpykfnqf24ge66t3a-r.redis.ap-mumbai-1.oci.oraclecloud.com"
replica_port = 6379

# Connect to the primary and replica Redis instances
primary = redis.StrictRedis(host=primary_host, port=primary_port, decode_responses=True, ssl=True, charset='utf-8')
replica = redis.StrictRedis(host=replica_host, port=replica_port, decode_responses=True, ssl=True, charset='utf-8')

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

# Test 1: Basic key-value read and write
print("Test 1: Basic key-value read and write")
primary.set("test_key", "Hello, OCI Cache!")
time.sleep(2)  # Allow time for replication
value = replica.get("test_key")
print(f"Value for test_key: {value}")

# Test 2: Incrementing a counter
print("Test 2: Incrementing a counter")
primary.set("counter", 0)
for _ in range(5):
    primary.incr("counter")
time.sleep(2)  # Allow time for replication
value = replica.get("counter")
print(f"Value for counter: {value}")

# Test 3: Working with sets
print("Test 3: Working with sets")
primary.sadd("fruits", "apple", "banana", "orange")
time.sleep(2)  # Allow time for replication
value = replica.smembers("fruits")
print(f"Value for fruits: {value}")

# Test 4: Working with lists
print("Test 4: Working with lists")
primary.rpush("tasks", "task_1", "task_2", "task_3")
time.sleep(2)  # Allow time for replication
value = replica.lrange("tasks", 0, -1)
print(f"Value for tasks: {value}")

# Test 5: Working with hashes
print("Test 5: Working with hashes")
primary.hset("user:1", mapping={"name": "John", "age": 30, "city": "New York"})
time.sleep(2)  # Allow time for replication
value = replica.hgetall("user:1")
print(f"Value for user:1: {value}")

# Test 6: Expiration and Time-To-Live (TTL)
print("Test 6: Expiration and Time-To-Live (TTL)")
temp_key = "temporary_key"
primary.set(temp_key, "Expires in 5 seconds")
primary.expire(temp_key, 5)
time.sleep(2)  # Allow time for replication
ttl = replica.ttl(temp_key)
print(f"Time to live for {temp_key}: {ttl} seconds")
time.sleep(5)  # Wait for the key to expire
value = replica.get(temp_key)
print(f"Value for {temp_key} after expiration: {value}")

# Test 7: Bulk insert and read
print("Test 7: Bulk insert and read")
num_records = 100
keys = []
for i in range(num_records):
    key = f"key_{i}"
    value = random_string(10)
    keys.append(key)
    primary.set(key, value)
time.sleep(2)  # Allow time for replication

print("Reading bulk-inserted records from the replica")
for key in keys:
    value = replica.get(key)
    if value is not None:
        print(f"Value for {key}: {value}")
    else:
        print(f"Key {key} not found")

# Test 8: Redis Pipelining
print("Test 8: Redis Pipelining")
num_records = 100
keys = [f"pipeline_key_{i}" for i in range(num_records)]
values = [random_string(10) for _ in range(num_records)]

# Pipeline write
print("Writing 100 records using pipeline")
pipe = primary.pipeline()
for key, value in zip(keys, values):
    pipe.set(key, value)
pipe.execute()
time.sleep(2)  # Allow time for replication

# Pipeline read
print("Reading 100 records using pipeline")
pipe = replica.pipeline()
for key in keys:
    pipe.get(key)
results = pipe.execute()

for key, value in zip(keys, results):
    if value is not None:
        print(f"Value for {key}: {value}")
    else:
        print(f"Key {key} not found")
