from flask import Flask, render_template, request, redirect, url_for, jsonify
import flask_login
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.validators import DataRequired
from database import db_session as db
from models import *
import bcrypt
import json
import os
from sqlalchemy import desc, func
#from urllib.parse import urlparse, urljoin



app = Flask(__name__)

app.secret_key = os.urandom(24)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

Bootstrap(app)

#class SecuredStaticFlask(Flask):
#	def send_static_file(self, filename):
#        # Get user from session
#		print('test', filename)
#		print(flask_login.current_user.is_authenticated())
#		if flask_login.current_user.is_authenticated():
#			return super(SecuredStaticFlask, self).send_static_file(filename)
#		else:
#			abort(403) 


#def is_safe_url(target):
#	ref_url = urlparse(request.host_url)
#	test_url = urlparse(urljoin(request.host_url, target))
#	return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

#def get_redirect_target():
#	for target in request.values.get('next'), request.referrer:
#		if not target:
#			continue
#		if is_safe_url(target):
#			return target

#def redirect_back(endpoint, **values):
#	target = request.form['next']
#	if not target or not is_safe_url(target):
#		target = url_for(endpoint, **values)
#	return redirect(target)




#def Username_check(form, field):
#	u = db.query(User).filter_by(username=field.data)
#	exists = u.scalar()
#	if type(form).__name__ == RegistrationForm and exists != None:
#		field.errors.append('Username already exists')
#		return False

#	if type(form).__name__ == LoginForm and exists == None:
#		field.errors.append('Username does not exist')
#		return False


class LoginForm(Form):
	username = StringField('Username', [validators.Length(min=3, max=25)], render_kw={"placeholder": "Username"})
	password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		u = db.query(User).filter_by(username=self.username.data)
		exists = u.scalar()
		if exists != None:
			if u.first().verify_password(self.password.data.encode()) == False:
				self.password.errors.append('Invalid password')
				return False
		else: 
			self.username.errors.append('Username does not exist')
			return False
		return True

class RegistrationForm(Form):
	username = StringField('Username', [validators.Length(min=3, max=25)],render_kw={"placeholder": "Username"})
	password = PasswordField('New Password', [validators.Length(min=3, max=72), validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')], render_kw={"placeholder": "Password"})
	confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Confirm Password"})

	def validate_username(form, field):
		u = db.query(User).filter_by(username=field.data)
		exists = u.scalar()
		if exists != None:
			raise ValidationError('Username already exists')


class DeleteAccForm(Form):
	username = StringField('Username', [validators.Length(min=3, max=25)])
	password = PasswordField('Current Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')],render_kw={"placeholder": "Password"})
	confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Confirm Password"})

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		u = db.query(User).filter_by(username=self.username.data)
		exists = u.scalar()
		if exists != None:
			if u.first().verify_password(self.password.data.encode()) == False:
				self.password.errors.append('Invalid password')
				return False
		else: 
			self.username.errors.append('Username does not exist')
			return False
		return True



class changePassForm(Form):
	username = StringField('Username', [validators.Length(min=3, max=25)])
	password = PasswordField('Current Password', [validators.DataRequired()], render_kw={"placeholder": "Current Password"})
	newpass = PasswordField('New Password', [validators.DataRequired(),validators.Length(min=3, max=72)], render_kw={"placeholder": "New Password"})

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		u = db.query(User).filter_by(username=self.username.data)
		exists = u.scalar()
		if exists != None:
			if u.first().verify_password(self.password.data.encode()) == False:
				self.password.errors.append('Invalid password')
				return False
			elif self.password.data == self.newpass.data:
				self.newpass.errors.append('New pass cannot be the same as old')
				return False
		else: 
			self.username.errors.append('Username does not exist')
			return False
		return True


@app.after_request
def add_header(response):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame, and also to cache the rendered page for 10 minutes.
	"""
	response.headers['Cache-Control'] = 'public, max-age=0'
	response.headers['Pragma'] = "no-cache"
	response.headers['Expires'] = "0"

	return response



@app.teardown_appcontext
def shutdown_session(exception=None):
	db.remove()


class Users(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(username):
	user_id = db.query(User).filter_by(username=username)

	if user_id.scalar() == None:
		return None

	user = Users()
	user.id = username
	return user


#@login_manager.request_loader
#def request_loader(request):
#	print('request: ', request.args)
#	username = request.form.get('username')
#	if username == None:
#		return
#	u = db.query(User).filter_by(username=username)
#	exists = u.scalar()
#	if exists == None:
#		return None
#	user = Users()
#	user.id = username
#	pw = request.form['password']
#	if len(pw) > 0:
#		verify = u.first().verify_password(pw.encode())
#		if verify == True:
#			user.is_authenticated = True
#			return user
#	return None


@app.route('/login', methods=['POST'])
def login():
#	next = get_redirect_target()
	form = LoginForm(request.form)
	if form.validate():
		user = Users()
		user.id = form.username.data
		flask_login.login_user(user)
		
#		if not is_safe_url(next):
#			return flask.abort(400)
	
		return redirect(url_for('home'))

	return render_template('home.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():

	if flask_login.current_user.is_authenticated == True:
		return redirect(url_for('home'))

#	next = get_redirect_target()

	

	form = RegistrationForm(request.form)

	if request.method == 'POST' and form.validate():
		
		pw = form.password.data
		new = pw.encode()
		hashed = bcrypt.hashpw(new, bcrypt.gensalt(13))
		u = User(form.username.data, hashed)
		db.add(u)
		db.commit()
		user = Users()
		user.id = form.username.data
		flask_login.login_user(user)
#		next = get_redirect_target()
#		if not is_safe_url(next):
#			return flask.abort(400)
		return redirect(url_for('home'))

	
	

	return render_template('register.html', form = form)


@app.route('/logout')
def logout():
	flask_login.logout_user()
	return redirect(url_for('home'))

@app.route('/deleteAccount', methods=['GET', 'POST'])
@flask_login.login_required
def deleteAccount():
	
#	next = get_redirect_target()
	form = DeleteAccForm(request.form)
	if request.method == 'GET':
		return render_template('deleteAccount.html', form=form)
	
	if request.method == 'POST' and form.validate():
#		userID = flask_login.current_user.get_id()
		u = db.query(User).filter_by(username=form.username.data).first()
		
		db.delete(u)
		db.commit()
		flask_login.logout_user()
		return redirect(url_for('home'))

	return render_template('deleteAccount.html', form=form)


@app.route('/changePass', methods=['GET', 'POST'])
@flask_login.login_required
def changePass():
	
#	next = get_redirect_target()
	form = changePassForm(request.form)
	if request.method == 'GET':
		return render_template('changePass.html', form=form)
	
	if request.method == 'POST' and form.validate():
		#		userID = flask_login.current_user.get_id()
		userID = form.username.data
		pw = form.newpass.data
		new = pw.encode()
		hashed = bcrypt.hashpw(new, bcrypt.gensalt(13))
		u = db.query(User).filter_by(username=userID).first()
		u.password = hashed
		db.commit()
		return redirect(url_for('home'))

	return render_template('changePass.html', form=form)




@login_manager.unauthorized_handler
def unauthorized_handler():
	return redirect(url_for('home'))


@app.route('/')
def index():
	return redirect(url_for('home'))


@app.route('/home')
def home():
#	next = get_redirect_target()
	form = LoginForm(request.form)
	return render_template('home.html', form = form)

@app.route('/flappypong', methods=['POST', 'GET'])
def flappypong():
	
	if request.method == 'POST':
		userID = flask_login.current_user.get_id()
		if request.json != "get" and userID != None:
			sub = db.query(FlappyPong.user_id, FlappyPong.score.label('score')).order_by(desc('score')).subquery()
			flaps = db.query(User.username, 'score').join((sub, sub.c.user_id==User.id)).filter(User.username==userID).all()
		
			count = 0
			found = False
			newScore = request.json
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.flappy_scores
			if len(flaps) < 5:
				u.flappy_scores.append(FlappyPong(score = newScore))
				db.commit()
			else:	
				if newScore > flaps[4][1]:
					found = False
					count = 0
					while not found and count < 5:
						if userScore[count].score == flaps[4][1]:
							db.delete(userScore[count])
							db.commit()
							found = True
						count += 1
					u.flappy_scores.append(FlappyPong(score = newScore))
					db.commit()

			userScore = db.query(User).filter_by(username = userID).first().flappy_scores
			
#		This is the old query:
#		flaps = db.query(FlappyPong).order_by(desc(FlappyPong.score)).limit(10).all()
		
#		This is the new query, which allows us to get just the top scores for each user, so we can support users having 
#		more than just one score in the database for any game table. 
		sub = db.query(FlappyPong.user_id, func.max(FlappyPong.score).label('user_max')).group_by(FlappyPong.user_id).order_by(desc('user_max')).limit(10).subquery()

		flaps = db.query(User.username, 'user_max').join((sub, sub.c.user_id==User.id)).all()
		global_top = {}
		personal_top = []
		for score in flaps:
			global_top[score[0]] = score[1]
		if userID != None:
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.flappy_scores
			for score in userScore:
				personal_top.append(score.score)
		else:
			personal_top.append('Anonymous user')
		scores = {"global_top": global_top, "personal_top": personal_top}
		return jsonify(scores)	
	return render_template('games/flappy_pong/flappy_pong.html')
#	return redirect(url_for('static', filename='games/flappy_pong/flappy_pong.html'))


@app.route('/gravitygolf', methods=['POST', 'GET'])
def gravitygolf():

	if request.method == 'POST':
		userID = flask_login.current_user.get_id()
		if request.json != "get" and userID != None:
			sub = db.query(GravityGolf.user_id, GravityGolf.score.label('score')).order_by(desc('score')).subquery()
			golfs = db.query(User.username, 'score').join((sub, sub.c.user_id==User.id)).filter(User.username==userID).all()
			count = 0
			found = False
			newScore = request.json
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.gravity_scores
			if len(golfs) < 5:
				u.gravity_scores.append(GravityGolf(score = newScore))
				db.commit()
			else:	
				if newScore < golfs[0][1]:
					found = False
					count = 0
					while not found and count < 5:
						if userScore[count].score == golfs[0][1]:
							db.delete(userScore[count])
							db.commit()
							found = True
						count += 1
					u.gravity_scores.append(GravityGolf(score = newScore))
					db.commit()
					found = True
			userScore = db.query(User).filter_by(username = userID).first().gravity_scores
		sub = db.query(GravityGolf.user_id, func.max(GravityGolf.score).label('user_max')).group_by(GravityGolf.user_id).order_by(desc('user_max')).limit(10).subquery()

		golfs = db.query(User.username, 'user_max').join((sub, sub.c.user_id==User.id)).all()
		global_top = {}
		personal_top = []
		for score in golfs:
			global_top[score[0]] = score[1]
		if userID != None:
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.gravity_scores
			for score in userScore:
				personal_top.append(score.score)
		else:
			personal_top.append('Anonymous user')
		scores = {"global_top": global_top, "personal_top": personal_top}
		return jsonify(scores)
	return render_template('games/GravityGolf/index.html')
	#return redirect(url_for('static', filename='games/GravityGolf/index.html'))


@app.route('/pacman', methods=['POST', 'GET'])
def pacman():

	if request.method == 'POST':
		userID = flask_login.current_user.get_id()
		
		if request.json != "get" and userID != None:
			sub = db.query(Pacman.user_id, Pacman.score.label('score')).order_by(desc('score')).subquery()
			pacs = db.query(User.username, 'score').join((sub, sub.c.user_id==User.id)).filter(User.username==userID).all()
			count = 0
			found = False
			newScore = request.json
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.pacman_scores
			if len(pacs) < 5:
				u.pacman_scores.append(Pacman(score = newScore))
				db.commit()
			else:	
				if newScore > pacs[4][1]:
					found = False
					count = 0
					while not found and count < 5:
						if userScore[count].score == pacs[4][1]:
							db.delete(userScore[count])
							db.commit()
							found = True
						count += 1
					u.pacman_scores.append(Pacman(score = newScore))
					db.commit()
					found = True
			userScore = db.query(User).filter_by(username = userID).first().pacman_scores
		
		sub = db.query(Pacman.user_id, func.max(Pacman.score).label('user_max')).group_by(Pacman.user_id).order_by(desc('user_max')).limit(10).subquery()

		pacs = db.query(User.username, 'user_max').join((sub, sub.c.user_id==User.id)).all()
		global_top = {}
		personal_top = []
		for score in pacs:
			global_top[score[0]] = score[1]
		if userID != None:
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.pacman_scores
			for score in userScore:
				personal_top.append(score.score)
		else:
			personal_top.append('Anonymous user')
		scores = {"global_top": global_top, "personal_top": personal_top}
		return jsonify(scores)


#	return render_template('games/pacman/index.html')
	return redirect(url_for('static', filename='javascript/pacman/index.html'))


@app.route('/lander', methods=['POST', 'GET'])
def lander():
	
	if request.method == 'POST':
		userID = flask_login.current_user.get_id()
		if request.json != "get" and userID != None:
			sub = db.query(Lander.user_id, Lander.score.label('score')).order_by(desc('score')).subquery()
			lands = db.query(User.username, 'score').join((sub, sub.c.user_id==User.id)).filter(User.username==userID).all()
			count = 0
			found = False
			newScore = request.json
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.lander_scores
			if len(lands) < 5:
				u.lander_scores.append(Lander(score = newScore))
				db.commit()
			else:	
				if newScore > lands[4][1]:
					found = False
					count = 0
					while not found and count < 5:
						if userScore[count].score == lands[4][1]:
							db.delete(userScore[count])
							db.commit()
							found = True
						count += 1
					u.lander_scores.append(Lander(score = newScore))
					db.commit()
					found = True
			userScore = db.query(User).filter_by(username = userID).first().lander_scores
			
		sub = db.query(Lander.user_id, func.max(Lander.score).label('user_max')).group_by(Lander.user_id).order_by(desc('user_max')).limit(10).subquery()

		lands = db.query(User.username, 'user_max').join((sub, sub.c.user_id==User.id)).all()
		global_top = {}
		personal_top = []
		for score in lands:
			global_top[score[0]] = score[1]
		if userID != None:
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.lander_scores
			for score in userScore:
				personal_top.append(score.score)
		else:
			personal_top.append('Anonymous user')
		scores = {"global_top": global_top, "personal_top": personal_top}
		return jsonify(scores)
	return render_template('games/lander.html')
	

@app.route('/fifteen', methods=['POST', 'GET'])
def fifteen():

	if request.method == 'POST':
		userID = flask_login.current_user.get_id()
		if request.json != "get" and userID != None:
			sub = db.query(Fifteen.user_id, Fifteen.score.label('score')).order_by(desc('score')).subquery()
			fifts = db.query(User.username, 'score').join((sub, sub.c.user_id==User.id)).filter(User.username==userID).all()
			count = 0
			found = False
			newScore = request.json
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.fifteen_scores
			if len(fifts) < 5:
				u.fifteen_scores.append(Fifteen(score = newScore))
				db.commit()
			else:
				if newScore < fifts[0][1]:
					found = False
					count = 0
					while not found and count < 5:
						if userScore[count].score == fifts[0][1]:
							db.delete(userScore[count])
							db.commit()
							found = True
						count += 1
					u.fifteen_scores.append(Fifteen(score = newScore))
					db.commit()
					found = True
			userScore = db.query(User).filter_by(username = userID).first().fifteen_scores
		
		sub = db.query(Fifteen.user_id, func.max(Fifteen.score).label('user_max')).group_by(Fifteen.user_id).order_by(desc('user_max')).limit(10).subquery()

		fifts = db.query(User.username, 'user_max').join((sub, sub.c.user_id==User.id)).all()
		global_top = {}
		personal_top = []
		for score in fifts:
			global_top[score[0]] = score[1]
		if userID != None:
			u = db.query(User).filter_by(username = userID).first()
			userScore = u.fifteen_scores
			for score in userScore:
				personal_top.append(score.score)
		else:
			personal_top.append('Anonymous user')
		scores = {"global_top": global_top, "personal_top": personal_top}
		return jsonify(scores)	

	return render_template('games/fifteen/index.html')
#	return redirect(url_for('static', filename='games/fifteen/index.html'))




@app.route('/api/flappypong')
def api_flappypong():
	flaps = db.query(FlappyPong).order_by(desc(FlappyPong.score)).all()
	
	scores = {}
	for score in flaps:
		scores[score.user.username] = {"score": score.score}
	return jsonify(scores);	


@app.route('/api/gravitygolf')
def api_gravitygolf():
	golfs = db.query(GravityGolf).order_by(desc(GravityGolf.score)).all()
	scores = {}
	for score in golfs:
		scores[score.user.username] = {"score": score.score}
	return jsonify(scores);	

@app.route('/api/pacman')
def api_pacman():
	pacs = db.query(Pacman).order_by(desc(Pacman.score)).all()
	scores = {}
	for score in pacs:
		scores[score.user.username] = {"score": score.score}
	return jsonify(scores);	

@app.route('/api/lander')
def api_lander():
	lands = db.query(Lander).order_by(desc(Lander.score)).all()
	scores = {}
	for score in lands:
		scores[score.user.username] = {"score": score.score}
	return jsonify(scores);	
	

@app.route('/api/fifteen')
def api_fifteen():
	fifteen = db.query(Fifteen).order_by(desc(Fifteen.score)).all()
	scores = {}
	for score in fifteen:
		scores[score.user.username] = {"score": score.score}
	return jsonify(scores);	







if __name__ == '__main__':
	app.run(debug='True',  host="0.0.0.0", port=8001)
