from flask_mongoengine import MongoEngine
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

db = MongoEngine()
# Class players.

class Player(db.Document):
	nombre_equipo = db.StringField(max_length=100)
	nombre = db.StringField(max_length=100)
	apellido = db.StringField(max_length=100)
	fecha_nacimiento = db.DateTimeField()
	posicion = db.StringField(max_length=50)
	camiseta = db.IntField(max_length=2)
	titular = db.BooleanField()
	foto = db.ImageField()

	meta = {
        'collection': 'players', # collection name
        'auto_create_index': False, # MongoEngine will not create index
        }

class Team(db.Document):
	nombre = db.StringField(max_length=100)
	bandera = db.ImageField()
	escudo = db.ImageField()
	pais = db.StringField(max_length= 30)

	meta = {
        'collection': 'teams', # collection name
        'auto_create_index': False, # MongoEngine will not create index
        }

class User(db.Document):
	_id = db.StringField(max_length=30)
	username = db.StringField(max_length=50)
	password_hash = db.StringField(max_length=200)

	meta = {
        'collection': 'users', # collection name
        'auto_create_index': False, # MongoEngine will not create index
        }

	def hash_password(self, password):
	    self.password_hash = pwd_context.encrypt(password)

	def get_secret(self, app):
		self.secret = app.config['SECRET_KEY']    

	def verify_password(self, password):
	    return pwd_context.verify(password, self.password_hash)	

	def generate_auth_token(self, app):
	    s = Serializer(app.config['SECRET_KEY'], expires_in = 6000)
	    #ide = str(self._id)
	    return s.dumps({ '_id': str(self._id) })

	@staticmethod
	def verify_auth_token(token,app):
	    s = Serializer(app.config['SECRET_KEY'])
	    # s = Serializer(secret)
	    try:
	        data = s.loads(token)
	    except SignatureExpired:
	        return None # valid token, but expired
	    except BadSignature:
	        return None # invalid token
	    user = User.objects(id = data['_id'])
	    return user