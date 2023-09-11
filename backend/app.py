import logging
import os
from flask import Flask
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_DB = os.environ.get('MONGO_DB', 'test')

# Connect to MongoDB
try:
    client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
    # client = MongoClient("mongodb://mongo:27017/")
    db = client[MONGO_DB]
    logging.info("Connected to MongoDB")
except Exception as e:
    logging.error(f"Could not connect to MongoDB: {e}")

@app.route('/')
def hello_world():
    try:
        db.my_collection.insert_one({"name": "John", "age": 30})
        logging.info("Document inserted")
    except Exception as e:
        logging.error(f"Could not insert document: {e}")
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
