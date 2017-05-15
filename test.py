from database import db_session as db
from models import *
from sqlalchemy import desc, func, distinct
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


#u = db.query(User).filter_by(username='poop').first()
#u.flappy_scores.append(FlappyPong(score = 1))
#db.commit()
#print(u.flappy_scores)

sub = db.query(FlappyPong.user_id, FlappyPong.score.label('score')).order_by(desc('score')).subquery()
flaps = db.query(User.username, 'score').join((sub, sub.c.user_id==User.id)).filter(User.username=="poop").all()
print(flaps)
#count = 0
#found = False
#newScore = 23
#u = db.query(User).filter_by(username = 'poop').first()
#userScore = u.flappy_scores
#if len(flaps) < 5:
#	u.flappy_scores.append(FlappyPong(score = newScore))
#	db.commit()
#else:	
#	while not found and count < 5:
#		if newScore > flaps[count][1]:
#			found2 = False
#			count2 = 0
#			while not found2 and count2 < 5:
#				if userScore[count2].score == flaps[count][1]:
#					db.delete(userScore[count2])
#					db.commit()
#					found2 = True
#				count2 += 1
#			u.flappy_scores.append(FlappyPong(score = newScore))
#			db.commit()
#			found = True
#		count += 1
#userScore = db.query(User).filter_by(username = 'poop').first().flappy_scores
#print(userScore)
#db.delete(userScore[0])
#db.commit()

#u = db.query(User).filter_by(username='josh').first()
#sub = db.query(FlappyPong.user_id, func.max(FlappyPong.score).label('user_max')).group_by(FlappyPong.user_id).order_by(desc('user_max')).limit(10).subquery()

#flaps = db.query(User.username, 'user_max').join((sub, sub.c.user_id==User.id)).all()
#db.commit()
#print(flaps)
#print(':::::::::::::::::::::')
#flaps = db.query(FlappyPong).order_by(desc(FlappyPong.score)).limit(10).all()
#print(flaps)

#print(u.verify_password(b"qwerty"))

#u.lander_scores.append(Lander(score = 14.5))
#db.commit()
#flaps = db.query(FlappyPong.score).all()
#userScore = db.query(User).filter_by(username = 'test').first().lander_scores
#print(userScore)
#for score in userScore:
#	db.delete(score)
#	db.commit()
#lands = db.query(FlappyPong).order_by(desc(FlappyPong.score)).limit(10).all()

#for score in lands:
#	db.delete(score)
#	db.commit()
#	print(score.score)


#print(lands[0].user.password)
#print(db.query(User).filter_by(username='test').first())
#print(db.query(User).filter_by(username='test').scalar())
