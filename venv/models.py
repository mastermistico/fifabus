from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
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

class Coach(db.Document):
	nombre_equipo = db.StringField(max_length=100)
	nombre = db.StringField(max_length=100)
	apellido = db.StringField(max_length=100)
	fecha_nacimiento = db.DateTimeField()
	nacionalidad = db.StringField(max_length= 30)
	rol = db.StringField(max_length= 30)
	meta = {
        'collection': 'coachs', # collection name
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
	password_hash = db.StringField(max_length=300)

	meta = {
        'collection': 'users', # collection name
        'auto_create_index': False, # MongoEngine will not create index
        }

	def hash_password(self, password):
	    self.password_hash = generate_password_hash(password, method='sha256')


	def get_secret(self, app):
		self.secret = app.config['SECRET_KEY']    

	def verify_password(self, password):
	    return pwd_context.verify(password, self.password_hash)