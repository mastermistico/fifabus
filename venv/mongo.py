from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'fifa'

app.config['MONGO_URI'] = 'mongodb//localhost:27017/fifa'

mongo = PyMongo(app)

CORS(app)

@app.route('/api/players', methods=['GET'])
def get_all_players():
#	players = mongo.db.players
#	result = []

#	for field in players.find():
#		result.append({'_id': str(field['_id']), 'title': field['title']})
	return jsonify({'hola': 'result'})

if __name__ == '__main__'

	app.run(debug=True)	
