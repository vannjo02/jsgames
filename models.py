from sqlalchemy import Table, Column, Float, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from database import Base
from models import *
import bcrypt

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True)
	password = Column(Text)
	lander_scores = relationship("Lander", cascade="all,delete,delete-orphan", backref = 'user', lazy='joined')
	flappy_scores = relationship("FlappyPong", cascade="all,delete,delete-orphan", backref = 'user', lazy='joined')
	gravity_scores = relationship("GravityGolf", cascade="all,delete,delete-orphan", backref = 'user', lazy='joined')
	pacman_scores = relationship("Pacman", cascade="all,delete,delete-orphan", backref = 'user', lazy='joined')
	fifteen_scores = relationship("Fifteen", cascade="all,delete,delete-orphan", backref = 'user', lazy='joined')

	def __init__(self, username, password):
		self.username = username
		self.password = password


	def __repr__(self):
		return "User({})".format(self.username)

	def verify_password(self, password):
#		old password checking:
#		pwhash = bcrypt.hashpw(password, self.password.decode('ascii'))


#		if bcrypt.checkpw(password, self.password.encode('ascii')):
		if bcrypt.checkpw(password, self.password):
			return True
		else: 
			return False


class Lander(Base):
	__tablename__ = 'lander'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))

	def __repr__(self):
		return "Lander({}, {})".format(self.user.username, self.score)

class FlappyPong(Base):
	__tablename__ = 'flappypong'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))

	def __repr__(self):
		return "FlappyPong({}, {})".format(self.user.username, self.score)

class GravityGolf(Base):
	__tablename__ = 'gravitygolf'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))

	def __repr__(self):
		return "GravityGolf({}, {})".format(self.user.username, self.score)

class Pacman(Base):
	__tablename__ = 'pacman'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))

	def __repr__(self):
		return "Pacman({}, {})".format(self.user.username, self.score)


class Fifteen(Base):
	__tablename__ = 'fifteen'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))

	def __repr__(self):
		return "Fifteen({}, {})".format(self.user.username, self.score)



