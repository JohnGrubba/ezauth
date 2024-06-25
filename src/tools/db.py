from pymongo import MongoClient
import os

DATABASE_URL = os.getenv("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client.get_database("ezauth")
users_collection = db.get_collection("users")

users_collection.create_index("email", unique=True)
users_collection.create_index("username", unique=True)
