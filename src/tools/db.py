from pymongo import MongoClient
import os

DATABASE_URL = os.getenv("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client.get_database("ezauth")
col = db.get_collection("users")

col.create_index("email", unique=True)
col.create_index("username", unique=True)
