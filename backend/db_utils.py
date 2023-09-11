from pymongo import MongoClient
import logging
from config import MONGO_HOST, MONGO_PORT, MONGO_DB

def init_db(app):
    try:
        client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
        app.config["db"] = client[MONGO_DB]
        logging.info("Connected to MongoDB")
    except Exception as e:
        logging.error(f"Could not connect to MongoDB: {e}")
