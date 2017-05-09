from database import db_session as db
from models import *
from sqlalchemy import desc
#import bcrypt

#new = "qwerty"
#new = new.encode()
#hashed = bcrypt.hashpw(new, bcrypt.gensalt(13))

#def verify_password(hashed, password):
#	pwhash = bcrypt.hashpw(password, hashed)
#	if len(hashed) != len(pwhash):
#		return False

#	result = 0
#	for x, y in zip(hashed, pwhash):
#		result |= x ^ y
#	return result == 0

#print(verify_password(hashed, b"qwerty"))

#u = User('username', hashed)
#db.add(u)
#db.commit()


#print('User.query.all(): ', User.query.all())
#print(User.query.all()[0].password)
#for user in User.query.all():
#	db.delete(user)
#db.commit()
#print('User.query.all(): ', User.query.all())




#print('User.query.get(1): ', User.query.get(1))


#print('db.query(User).filter_by(password="password").first(): ', db.query(User).filter_by(password="password").first())

#u = db.query(User).filter_by(username='test').first()
#print(u)
#print(u.verify_password(b"qwerty"))

#u.lander_scores.append(Lander(score = 14.5))
#db.commit()
#lands = db.query(Lander.score).order_by
userScore = db.query(User).filter_by(username = 'test').first().lander_scores
print(userScore)
#for score in userScore:
#	db.delete(score)
#	db.commit()
#lands = db.query(Lander).order_by(desc(Lander.score)).limit(10).all()
#for score in lands:
#	db.delete(score)
#	db.commit()
#	print(score.user.username)


#print(lands[0].user.password)
#print(db.query(User).filter_by(username='test').first())
#print(db.query(User).filter_by(username='test').scalar())
