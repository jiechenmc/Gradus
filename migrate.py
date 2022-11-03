from pymongo import MongoClient
import os

# Mongo Setup
client = MongoClient(os.getenv("mongo_url"))
db = client.get_database("Gradus")
collection = db.get_collection("Spring 2022")

with open("data.json", "r") as f:
    pass