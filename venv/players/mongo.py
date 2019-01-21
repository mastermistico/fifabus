from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'fifa'

app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/fifa'

mongo = PyMongo(app)

CORS(app)

@app.route('/api/players', methods=['GET'])
def get_all_players():
	players = mongo.db.players
	result = []

	for field in players.find():
		result.append({
						'_id': str(field['_id']), 
						'nombre': field['nombre']})
	return jsonify(result)

@app.route('/api/players', methods=['POST'])
def add_players():
	players = mongo.db.players

	player = {
		'nombre' : request.get_json()['nombre'],
		'apellido' : request.get_json()['apellido'],
		'fecha_nacimiento' : request.get_json()['fecha_nacimiento'],
		'posicion' : request.get_json()['posicion'],
		'camiseta' : request.get_json()['camiseta'],
		'titular' : request.get_json()['titular']
		#	foto = request.get_json()['foto']
	}

	players_id = players.insert(player)

	return jsonify({'result': 'OK'})

if __name__ == '__main__':
	app.run(debug=True)	

