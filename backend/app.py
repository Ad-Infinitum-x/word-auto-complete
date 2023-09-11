import logging
import os
from cachetools import LRUCache
from flask import Flask
from pymongo import MongoClient
from requests import get
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

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

# @app.route('/')
# def hello_world():
#     try:
#         logging.info("Document inserted")
#     except Exception as e:
#         logging.error(f"Could not insert document: {e}")
#     return 'Hello, World!'

cache = LRUCache(maxsize=100)

def bpe_autocomplete(input_text, bpe_model):
    last_subword = extract_last_subword(input_text)
    
    # Directly look up in bpe_model
    suggestions = [word for word in bpe_model.keys() if last_subword in word]
    
    return suggestions


@app.route('/autocomplete/<string:input_text>', methods=['GET'])
def autocomplete(input_text):
    suggestions = bpe_autocomplete(input_text, bpe_model)
    return {"suggestions": suggestions}

def get_stats(vocab):
    pairs = {}
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pair = (symbols[i], symbols[i+1])
            if pair in pairs:
                pairs[pair] += freq
            else:
                pairs[pair] = freq
    return pairs

def merge_vocab(pair, vocab):
    new_vocab = {}
    replacement = f"{pair[0]}{pair[1]}"
    pattern = re.compile(r'(?<!\S)' + re.escape(f"{pair[0]} {pair[1]}") + r'(?!\S)')
    for word in vocab:
        new_word = re.sub(pattern, replacement, word)
        new_vocab[new_word] = vocab[word]
    return new_vocab

import re

def train_bpe(corpus, vocab_size):
    # Tokenize the corpus into a vocabulary
    vocab = {}
    for word in corpus.split():
        word = ' '.join(list(word)) + ' </w>'
        if word in vocab:
            vocab[word] += 1
        else:
            vocab[word] = 1
            
    for i in range(vocab_size):
        pairs = get_stats(vocab)
        if not pairs:
            break
        best_pair = max(pairs, key=pairs.get)
        vocab = merge_vocab(best_pair, vocab)
    
    # The final vocabulary (subword units)
    return {k: v for k, v in vocab.items() if len(k.split()) == 1}

bpe_model = train_bpe("hello, hella, helli, testing", vocab_size=1000)

def bpe_autocomplete(input_text, bpe_model):
    last_subword = extract_last_subword(input_text)
    
    # Directly look up in bpe_model
    suggestions = [word for word in bpe_model.keys() if last_subword in word]
    
    return suggestions

def extract_last_subword(input_text, length=3):
    return input_text[-length:]

def is_new_subword(subword, bpe_model):
    return subword not in bpe_model.subwords

def update_bpe_model(new_text, bpe_model):
    updated_corpus = new_text  # Add logic to combine with old corpus
    vocab_size = len(bpe_model)  # Or set to a new size if you want the vocab to grow
    new_vocab = train_bpe(updated_corpus, vocab_size)
    return new_vocab

def save_bpe_to_mongo(db, bpe_model):
    collection = db['test']
    collection.insert_one({"vocab": bpe_model})

def load_bpe_from_mongo(db):
    collection = db['bpe_vocab']
    latest_entry = collection.find_one(sort=[('_id', -1)])
    if latest_entry:
        return latest_entry['vocab']
    else:
        return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

