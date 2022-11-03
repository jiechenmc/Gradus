from json import loads
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Mongo Setup
load_dotenv()
client = MongoClient(os.getenv("mongo_url"))
db = client.get_database("Gradus")
collection = db.get_collection("Spring 2022")

with open("data.json", "r") as f:
    lines = f.readlines()
    data = list(map(loads, lines))
    collection.insert_many(data)