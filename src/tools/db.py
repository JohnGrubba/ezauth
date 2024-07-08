from pymongo import MongoClient
import os, bson.json_util, json
from tools.conf import SessionConfig

DATABASE_URL = os.getenv("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client.get_database("ezauth")
users_collection = db.get_collection("users")
sessions_collection = db.get_collection("sessions")

# Find Users by email and username fast (id is already indexed)
users_collection.create_index("email", unique=True)
users_collection.create_index("username", unique=True)
# Find Sessions by session_token fast
sessions_collection.create_index("session_token", unique=True)

try:
    sessions_collection.drop_index("createdAt_1")
except:
    pass
# Set TTL For Sessions
sessions_collection.create_index(
    "createdAt", expireAfterSeconds=SessionConfig.session_expiry_seconds
)


def bson_to_json(data: bson.BSON) -> dict:
    """Convert BSON to JSON. Also converts the _id to a string.

    Args:
        data (bson.BSON): BSON Data

    Returns:
        dict: JSON Data
    """
    original_json = json.loads(bson.json_util.dumps(data))
    original_json["_id"] = str(original_json["_id"]["$oid"])
    return original_json
