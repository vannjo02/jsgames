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
	lander_scores = relationship("Lander", back_populates = 'user')
	flappy_scores = relationship("FlappyPong", back_populates = 'user')
	gravity_scores = relationship("GravityGolf", back_populates = 'user')
	pacman_scores = relationship("Pacman", back_populates = 'user')
	fifteen_scores = relationship("Fifteen", back_populates = 'user')

	def __init__(self, username, password):
		self.username = username
		self.password = password


	def __repr__(self):
		return "User({})".format(self.username)

	def verify_password(self, password):
		pwhash = bcrypt.hashpw(password, self.password)
		if len(self.password) != len(pwhash):
			return False

		result = 0
		for x, y in zip(self.password, pwhash):
			result |= x ^ y
		return result == 0


class Lander(Base):
	__tablename__ = 'lander'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship("User", back_populates = "lander_scores")

	def __repr__(self):
		return "Lander({}, {})".format(self.user.username, self.score)

class FlappyPong(Base):
	__tablename__ = 'flappypong'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship("User", back_populates = "flappy_scores")

	def __repr__(self):
		return "FlappyPong({}, {})".format(self.user.username, self.score)

class GravityGolf(Base):
	__tablename__ = 'gravitygolf'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship("User", back_populates = "gravity_scores")

	def __repr__(self):
		return "GravityGolf({}, {})".format(self.user.username, self.score)

class Pacman(Base):
	__tablename__ = 'pacman'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship("User", back_populates = "pacman_scores")

	def __repr__(self):
		return "Pacman({}, {})".format(self.user.username, self.score)


class Fifteen(Base):
	__tablename__ = 'fifteen'
	id = Column(Integer, primary_key=True)
	score = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship("User", back_populates = "fifteen_scores")

	def __repr__(self):
		return "Fifteen({}, {})".format(self.user.username, self.score)



