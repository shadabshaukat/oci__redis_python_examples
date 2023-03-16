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
import json
import threading

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

# Test 9: Large data payload
print("Test 9: Large data payload")
large_key = "large_data"
large_data = {f"field_{i}": random_string(1000) for i in range(1000)}
primary.set(large_key, json.dumps(large_data))
time.sleep(2)  # Allow time for replication
value = replica.get(large_key)
loaded_data = json.loads(value)
print(f"Loaded {len(loaded_data)} fields from {large_key}")

# Test 10: Sorted sets for ranking
print("Test 10: Sorted sets for ranking")
users = [f"user_{i}" for i in range(100)]
scores = [random.randint(0, 1000) for _ in range(100)]

# Add users and scores to sorted set
for user, score in zip(users, scores):
    primary.zadd("leaderboard", {user: score})
time.sleep(2)  # Allow time for replication

# Get top 10 users
top_users = replica.zrevrange("leaderboard", 0, 9, withscores=True)
print("Top 10 users in the leaderboard:")
for rank, (user, score) in enumerate(top_users, start=1):
    print(f"{rank}. {user}: {score}")

# Test 11: Publish and Subscribe (Pub/Sub)
print("Test 11: Publish and Subscribe (Pub/Sub)")
pubsub = replica.pubsub(ignore_subscribe_messages=True)
pubsub.subscribe("news")

def print_message(message):
    print(f"Message received: {message['data']}")

def listen(pubsub):
    for message in pubsub.listen():
        print_message(message)

t = threading.Thread(target=listen, args=(pubsub,))
t.start()

primary.publish("news", "Breaking news!")
time.sleep(2)  # Allow time for message propagation
pubsub.unsubscribe("news")
t.join()

# Set the initial value of the "counter" key
primary.set("counter", 0)

# Test 12: Transactions
print("Test 12: Transactions")
with primary.pipeline() as pipe:
    while True:
        try:
            # watch the counter key
            pipe.watch("counter")
            counter_value = int(pipe.get("counter"))
            new_counter_value = counter_value + 1
            pipe.multi()
            pipe.set("counter", new_counter_value)
            pipe.execute()
            break
        except redis.WatchError:
            continue
time.sleep(2)  # Allow time for replication
print(f"New value for counter: {replica.get('counter')}")

# Test 13: Geospatial indexes
print("Test 13: Geospatial indexes")
geo_data = [
    ("Sydney", -33.8688, 151.2093),
    ("Melbourne", -37.8136, 144.9631),
    ("Brisbane", -27.4698, 153.0251),
    ("Perth", -31.9505, 115.8605),
    ("Adelaide", -34.9285, 138.6007),
    ("Gold Coast", -28.0167, 153.4000),
    ("Canberra", -35.2809, 149.1300),
    ("Newcastle", -32.9267, 151.7765),
    ("Hobart", -42.8821, 147.3272),
]

for city, lat, lon in geo_data:
    primary.execute_command("GEOADD", "cities", lon, lat, city)
time.sleep(2)  # Allow time for replication

# Calculate and print the distance between all major cities in Australia
for i, (city1, lat1, lon1) in enumerate(geo_data):
    for j, (city2, lat2, lon2) in enumerate(geo_data[i + 1:]):
        distance = replica.geodist("cities", city1, city2, unit="km")
        print(f"Distance between {city1} and {city2}: {distance} km")


# Test 14: LUA Scripting
print("Test 14: LUA Scripting")
lua_script = """
local value = redis.call("GET", KEYS[1])
value = tonumber(value) * ARGV[1]
redis.call("SET", KEYS[1], value)
return value
"""

# Define a Lua script object
multiply_by = primary.register_script(lua_script)
key_to_multiply = "counter"
factor = 2

# Execute the Lua script on the primary Redis instance
result = multiply_by(keys=[key_to_multiply], args=[factor])
print(f"Value of {key_to_multiply} multiplied by {factor}: {result}")

time.sleep(2)  # Allow time for replication
print(f"New value for {key_to_multiply} in replica: {replica.get(key_to_multiply)}")


# Test 15: HyperLogLog
print("Test 15: HyperLogLog")
unique_users_key = "unique_users"

# Simulate 10,000 unique users visiting the site
unique_users = [f"user_{i}" for i in range(10000)]

# Simulate 1,000 users visiting the site multiple times
for user in unique_users:
    for _ in range(random.randint(1, 5)):
        primary.pfadd(unique_users_key, user)

time.sleep(2)  # Allow time for replication

# Get the estimated count of unique users
estimated_unique_users = replica.pfcount(unique_users_key)
print(f"Estimated unique users count: {estimated_unique_users}")

# Cleanup: Deleting keys created during the tests
print("Cleaning up keys created during the tests")
primary.flushdb()
