from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("WARNING: No MONGO_URI found in .env file!")

client = MongoClient(MONGO_URI)
db = client.get_database("kindlinkbridge") 