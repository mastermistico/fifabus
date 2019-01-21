from flask import Flask, jsonify, request, g, url_for, abort
from bson.objectid import ObjectId
from flask_cors import CORS
from models import db, Player, Team, User
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


app = Flask(__name__)

#app.config['MONGO_DBNAME'] = 'fifa'
#app.config['MONGO_URI'] = 'mongodb//localhost:27017/fifa'
app.config['SECRET_KEY'] = 'uno se muere y nada se lleva'
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/fifa'
app.debug = True
db.init_app(app)

CORS(app)

######################################################################################
# source example
######################################################################################
#@app.route('/api/resource')
#@auth.login_required
#def get_resource():
#    return jsonify({ 'data': 'Hello, %s!' % g.user.username })
######################################################################################
#verify pass
######################################################################################    
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token,app)
    if not user:
        # try to authenticate with username/password
        user = User.objects(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    user.get_secret(app)
    g.user = user
    return True
######################################################################################
#get token
######################################################################################
@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(app)
    return jsonify({ 'token': token.decode('ascii') })    
######################################################################################
# user registration
######################################################################################
@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        jsonify({'err':'miss'})
    	#abort(401) # missing arguments
    if User.objects(username = username).limit(1) is not None:
        #abort(402) # existing user
        jsonify({'err':'exis'})
    user = User(username = username)
    user.hash_password(password)
    user.save()
    return jsonify({ 'username': user.username })
    #return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user._id, _external = True)}    
######################################################################################
@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.objects.get(_id=id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})
######################################################################################
# get total players
######################################################################################
@app.route('/api/players/total', methods=['GET'])
def get_total():
	total = Player.objects.count()

	return jsonify({'total': total})
######################################################################################
# get old player
######################################################################################
@app.route('/api/players/old', methods=['GET'])
def get_old_players():
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
def get_young_players():
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
def get_suplent():
	alternate = Player.objects(titular = False).count()

	return jsonify({'alternate_players': alternate})		
######################################################################################
# get avg players 
######################################################################################
@app.route('/api/players/avgalter', methods=['GET'])
def get_avg():
	result = []
	avg_alter = Player.objects(titular = False).distinct('nombre_equipo')
	
	for field in avg_alter:
		result.append({
				'equipo': field
			})

		return jsonify(result)
######################################################################################
# save players info
######################################################################################
@app.route('/api/players', methods=['POST'])
def add_players():

	#	foto = request.get_json()['foto']
	
	player_new = Player(nombre_equipo = request.get_json()['nombre_equipo'],
						nombre = request.get_json()['nombre'],
						apellido = request.get_json()['apellido'],
						fecha_nacimiento = request.get_json()['fecha_nacimiento'],
						posicion = request.get_json()['posicion'],
						camiseta = request.get_json()['camiseta'],
						titular = request.get_json()['titular'])
	try:	
		player_new.save()
		return jsonify({'result': 'OK'})
	except(ValueError, KeyError, TypeError):
		return jsonify({'result': 'error'})	
######################################################################################
# get teams 
######################################################################################
@app.route('/api/teams', methods=['GET'])
def get_all_teams():
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
def add_teams():
	result = []
	team_new = Team(nombre = request.get_json()['nombre'])
	try:
		team_new.save()
		return jsonify({'result': 'OK'})
	except(ValueError, KeyError, TypeError):		
		return jsonify({'result': 'error'})

if __name__ == '__main__':
	app.run(debug=True)		