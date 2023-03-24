from json import dumps
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Mongo Setup
load_dotenv()
client = MongoClient(os.getenv("mongo_url"))
db = client.get_database(os.getenv("mongo_db"))

if not os.path.exists("export"):
    os.makedirs("export")

for col in db.list_collection_names():
    curr = db.get_collection(col)
    with open(f"export/{col}.json", "w+") as f:
        entries = list(curr.find({}, {"_id": False}))
        f.write("[")
        for i, entry in enumerate(entries):
            if (i != len(entries) - 1):
                f.write(dumps(entry) + ",\n")
            else:
                f.write(dumps(entry) + "\n")
        f.write("]")