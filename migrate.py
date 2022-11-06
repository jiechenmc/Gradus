from json import loads
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Mongo Setup
load_dotenv()
client = MongoClient(os.getenv("mongo_url"))
db = client.get_database(os.getenv("mongo_db"))

with open("data.json", "r") as f:
    lines = f.readlines()
    data = list(map(loads, lines))
    collection = db.get_collection(data[0]["Term"])
    collection.insert_many(data)

clear = input("Clear .cache and data.json? (y,n) ").lower()

if clear == "y":
    try:
        os.remove(".cache")
        os.remove("data.json")
        print("Cleared...")
    except FileNotFoundError:
        print("Files might've already been cleared")