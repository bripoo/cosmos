from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

# Configuration variables
COSMOS_DB_URI = "mongodb://bripo-mongo:RHsQz61gKl7MROETiMLkar2FLOXvxOHvWcoEfOkwegLOLo8M0RLMQD0708K5BbayxfyF8i5vVqsjACDbRohFcA==@bripo-mongo.mongo.cosmos.azure.com:10255/brij?ssl=true&replicaSet=globaldb&retryWrites=false&maxIdleTimeMS=120000"
DATABASE_NAME = 'brij'
COLLECTION_NAME = 'TP1'
PORT = int(os.getenv("PORT", 5000))

# Initialize Flask app
app = Flask(__name__)

# Initialize MongoDB client
client = MongoClient(COSMOS_DB_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def home():
    # Insert a document with the shard key
    result = collection.insert_one({"TPZ": "India", "name": "Brijesh", "Location": "Mumbai"})
    return "Welcome to the Flask Azure Cosmos DB API!"

@app.route('/items', methods=['GET'])
def get_items():
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
    return jsonify(items), 200

@app.route('/items', methods=['POST'])
def add_item():
    item = request.json
    result = collection.insert_one(item)
    return jsonify({'inserted_id': str(result.inserted_id)}), 201

@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    item = collection.find_one({"_id": item_id})
    if item:
        item['_id'] = str(item['_id'])
        return jsonify(item), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    item = request.json
    result = collection.update_one({"_id": item_id}, {"$set": item})
    if result.matched_count:
        return jsonify({'msg': 'Item updated'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    result = collection.delete_one({"_id": item_id})
    if result.deleted_count:
        return jsonify({'msg': 'Item deleted'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
