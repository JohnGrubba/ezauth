from pymongo import MongoClient
import os
from tools.conf import SessionConfig

DATABASE_URL = os.getenv("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client.get_database("ezauth")
users_collection = db.get_collection("users")
sessions_collection = db.get_collection("sessions")

users_collection.create_index("email", unique=True)
users_collection.create_index("username", unique=True)
sessions_collection.create_index("session_token", unique=True)

sessions_collection.drop_index("createdAt_1")
# Set TTL For Sessions
sessions_collection.create_index(
    "createdAt", expireAfterSeconds=SessionConfig.session_expiry_seconds
)
