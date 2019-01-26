from flask import Flask, jsonify, request, g, url_for, abort, make_response
from bson import ObjectId, json_util
from flask_cors import CORS
from models import db, Player, Team, User, Coach
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from json import dumps
import requests

auth = HTTPBasicAuth()


app = Flask(__name__)

#app.config['MONGO_DBNAME'] = 'fifa'
#app.config['MONGO_URI'] = 'mongodb//localhost:27017/fifa'
app.config['SECRET_KEY'] = 'unosemuereynadaselleva'
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/fifa'
app.debug = True
db.init_app(app)

#CORS(app)



######################################################################################
#validate token
######################################################################################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.objects(_id=data['some']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated    
######################################################################################
# login registration
######################################################################################
@app.route('/api/login', methods = ['POST'])
def login():
	auth = request.get_json()
	print(auth)
	if not auth or not auth['username'] or not auth['password']:
		return make_response('Could not verify auth', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

	user = User.objects(username=auth['username']).first()	
	if not user:
		return make_response('Could not verify not user', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

	if check_password_hash(user['password_hash'], auth['password']):
		idd= str(user['_id'])
		token = jwt.encode({'some': idd }, app.config['SECRET_KEY'], algorithm='HS256')
		return jsonify({'token' : token.decode('UTF-8')})

	return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})     
######################################################################################
# user registration
######################################################################################
@app.route('/api/users', methods = ['POST'])
def new_user():
    data = request.get_json()
    if data['username'] is None or data['password'] is None:
    	#abort(401) # missing arguments
    	make_response('missing arguments', 401, {'arguments': data})
    if User.objects(username = data['username']).first() is not None:
    	make_response('existing user', 401, {'user': data['username']})
        #abort(401) # existing user
    user = User(username=data['username'])
    user.hash_password(data['password'])
    user.save()
    return jsonify({ 'username': user.username })
    #return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user._id, _external = True)}    
######################################################################################
# get total players
######################################################################################
@app.route('/api/players/total', methods=['GET'])
@token_required
def get_total(current_user):
	total = Player.objects.count()

	return jsonify({'total': total})
######################################################################################
# get old player
######################################################################################
@app.route('/api/players/old', methods=['GET'])
@token_required
def get_old_players(current_user):
	result = []
	old = Player.objects().order_by('fecha_nacimiento').limit(1)

	return jsonify({'player_old':{
					'nombre': old[0].nombre,
					'apellido': old[0].apellido
				  }})	
######################################################################################
# get young player
######################################################################################
@app.route('/api/players/young', methods=['GET'])
@token_required
def get_young_players(current_user):
	result = []
	young = Player.objects().order_by('-fecha_nacimiento').limit(1)

	return jsonify({'player_young': {
						'nombre': young[0].nombre,
						'apellido': young[0].apellido
					}})	
######################################################################################
# get suplent players
######################################################################################
@app.route('/api/players/alternate', methods=['GET'])
@token_required
def get_suplent(current_user):
	alternate = Player.objects(titular = False).count()

	return jsonify({'alternate_players': alternate})		
######################################################################################
# get avg players 
######################################################################################
@app.route('/api/players/avgalter', methods=['GET'])
@token_required
def get_avg(current_user):
	result = []
	avg_alter = Player.aggregate([
			{'$group': 
				{
					'_id': {'nombre_equipo': '$team'},
					'avg' : { '$avg' : 1}
				}
			}
		])
	
	for field in avg_alter:
		result.append({
				'equipo': field._id.nombre_equipo,
				'avg': field.avg
			})

		return jsonify(result)
######################################################################################
# save players info
######################################################################################
@app.route('/api/players', methods=['POST'])
@token_required
def add_players(current_user):

	#	foto = request.get_json()['foto']
	
	player_new = Player(nombre_equipo = request.form['nombreEquipo'],
						nombre = request.form['nombre'],
						apellido = request.form['apellido'],
						fecha_nacimiento = request.form['nacimiento'],
						posicion = request.form['posicion'],
						camiseta = request.form['camiseta'],
						titular = request.form['titular'],
						foto = request.files['files0'])
	try:	
		player_new.save()
		return jsonify({'result': 'OK'})
	except(ValueError, KeyError, TypeError):
		return jsonify({'result': 'error'})	
######################################################################################
# save coachs info
######################################################################################
@app.route('/api/coachs', methods=['POST'])
@token_required
def add_coachs(current_user):

	coach_new = Coach(	nombre_equipo = request.get_json()['nombreEquipo'],
						nombre = request.get_json()['nombre'],
						apellido = request.get_json()['apellido'],
						fecha_nacimiento = request.get_json()['nacimiento'],
						rol = request.get_json()['rol'],
						nacionalidad = request.get_json()['nacionalidad'])
	try:	
		coach_new.save()
		return jsonify({'result': 'OK'})
	except(ValueError, KeyError, TypeError):
		return jsonify({'result': 'error'})			
######################################################################################
# get teams 
######################################################################################
@app.route('/api/teams', methods=['GET'])
@token_required
def get_all_teams(current_user):
	result = []
	# request.args.get('')
	for field in Team.objects():
		result.append({
						'nombre': field['nombre']
			})
	try:		
		return jsonify(result)	
	except(ValueError, KeyError, TypeError):		
		return jsonify({'result': 'error'})
######################################################################################
# save teams info
######################################################################################
@app.route('/api/teams', methods=['POST'])
@token_required
def add_teams(current_user):
	result = []
	print(request.get_json())
	team_new = Team(nombre = request.form['nombre'],
					pais= request.form['pais'],
					bandera= request.files['files0'],
					escudo= request.files['files1'])
	try:
		team_new.save()
		return jsonify({'result': 'OK'})
	except(ValueError, KeyError, TypeError):		
		return jsonify({'result': 'error'})
######################################################################################
# country
######################################################################################
@app.route('/api/country')
def get_data():
    return requests.get('https://restcountries.eu/rest/v2/all').content

if __name__ == '__main__':
	app.run(debug=True)		