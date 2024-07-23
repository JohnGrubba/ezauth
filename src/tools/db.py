from pymongo import MongoClient
import os
import bson.json_util
import json
from tools.conf import SessionConfig
import redis
import logging
import sys
from mongomock import MongoClient as MongoTestClient
import fakeredis

logger = logging.getLogger("uvicorn.info")

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")

logger.info("\u001b[34mConnecting to Redis...\u001b[0m")
if "pytest" in sys.modules:
    r = fakeredis.FakeRedis()
else:
    r = redis.Redis(host=REDIS_HOST, decode_responses=True, password=REDIS_PASSWORD)
logger.info("\u001b[32m+ Connected to Redis\u001b[0m")
logger.info("\u001b[34mConnecting to MongoDB...\u001b[0m")
if "pytest" in sys.modules:
    client = MongoTestClient()
else:
    client = MongoClient(DATABASE_URL)
logger.info("\u001b[32m+ Connected to MongoDB\u001b[0m")
db = client.get_database("ezauth")
users_collection = db.get_collection("users")
sessions_collection = db.get_collection("sessions")

# Find Users by email and username fast (id is already indexed)
users_collection.create_index("email", unique=True)
users_collection.create_index("username", unique=True)
users_collection.create_index("google_uid", unique=True, sparse=True)
users_collection.create_index("github_uid", unique=True, sparse=True)
# Find Sessions by session_token fast
sessions_collection.create_index("session_token", unique=True)

try:
    sessions_collection.drop_index("createdAt_1")
except Exception:
    pass
# Set TTL For Sessions
sessions_collection.create_index(
    "createdAt", expireAfterSeconds=SessionConfig.session_expiry_seconds
)


def bson_to_json(data: bson.BSON) -> dict:
    """Convert BSON to JSON. From MongoDB to JSON.

    Args:
        data (bson.BSON): BSON Data

    Returns:
        dict: JSON Data
    """
    if not data:
        return None
    original_json = json.loads(bson.json_util.dumps(data))
    # Iterate over the keys and convert the _id to a string
    for key in original_json:
        if isinstance(original_json[key], dict):
            if len(list(original_json[key].keys())) == 0:
                continue
            if list(original_json[key].keys())[0] == "$oid":
                original_json[key] = str(original_json[key]["$oid"])
            elif list(original_json[key].keys())[0] == "$date":
                original_json[key] = str(original_json[key]["$date"])
    return original_json
