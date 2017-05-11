from flask import Flask, render_template, request, redirect, url_for, jsonify
import flask_login
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.validators import DataRequired
import os
from database import db_session as db
from models import *
import bcrypt
import json
from urllib.parse import urlparse, urljoin
from sqlalchemy import desc

app = Flask(__name__)
#os.urandom(24)
app.secret_key = '\x1fy\xb0[\x85\xf2\xe5\xd4\x94\x06F\xd9\x1dd\x93\x14\xde\xb1\x12H\xa2\x15V\x90'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

Bootstrap(app)

class SecuredStaticFlask(Flask):
	def send_static_file(self, filename):
        # Get user from session
		print('test', filename)
		print(flask_login.current_user.is_authenticated())
		if flask_login.current_user.is_authenticated():
			return super(SecuredStaticFlask, self).send_static_file(filename)
		else:
			abort(403) 


def is_safe_url(target):
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))
	return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def get_redirect_target():
	for target in request.values.get('next'), request.referrer:
		if not target:
			continue
		if is_safe_url(target):
			return target

def redirect_back(endpoint, **values):
	target = request.form['next']
	if not target or not is_safe_url(target):
		target = url_for(endpoint, **values)
	return redirect(target)




def Username_check(form, field):
	u = db.query(User).filter_by(username=field.data)
	exists = u.scalar()
	if type(form).__name__ == RegistrationForm and exists != None:
		field.errors.append('Username already exists')
		return False

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
	username = StringField('Username', [validators.Length(min=3, max=25), Username_check],render_kw={"placeholder": "Username"})
	password = PasswordField('New Password', [validators.Length(min=3, max=72), validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')], render_kw={"placeholder": "Password"})
	confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Confirm Password"})

	def validate_username(form, field):
		u = db.query(User).filter_by(username=field.data)
		exists = u.scalar()
		if exists != None:
			raise ValidationError('Username already exists')


class DeleteAccForm(Form):
	password = PasswordField('Current Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')


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


@login_manager.request_loader
def request_loader(request):
	print('test2', request.args)
	username = request.form.get('username')
	if username == None:
		return
	u = db.query(User).filter_by(username=username)
	exists = u.scalar()
	if exists == None:
		return None
	user = Users()
	user.id = username
	pw = request.form['password']
	if len(pw) > 0:
		verify = u.first().verify_password(pw.encode())
		if verify == True:
			user.is_authenticated = True
	return None


@app.route('/login', methods=['POST'])
def login():
	next = get_redirect_target()
	form = LoginForm(request.form)
	if form.validate():
		user = Users()
		user.id = form.username.data
		flask_login.login_user(user)
		return redirect_back('home')

	return render_template('home.html', form = form, next=next)


@app.route('/register', methods=['GET', 'POST'])
def register():

	next = get_redirect_target()

	if flask_login.current_user.is_authenticated == True:
		return redirect(url_for('home'))

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
		return redirect_back('home')

	
	

	return render_template('register.html', form = form, next = next)


@app.route('/logout')
def logout():
	flask_login.logout_user()
	return redirect(url_for('home'))

@app.route('/deleteAccount', methods=['GET', 'POST'])
@flask_login.login_required
def deleteAccount():
	next = get_redirect_target()
	form = DeleteAccForm(request.form)
	if request.method == 'GET':
		return render_template('deleteAccount.html', form=form)

	if request.method == 'POST' and form.validate():
		userID = flask_login.current_user.get_id()
		u = db.query(User).filter_by(username=userID).first()
		if u.verify_password(form.password.data.encode()):
			db.delete(u)
			db.commit()
			flask_login.logout_user()
			return redirect(url_for('home'))

	return render_template('deleteAccount.html', form=form)


@login_manager.unauthorized_handler
def unauthorized_handler():
	return redirect(url_for('home'))


@app.route('/')
def index():
	return redirect(url_for('home'))


@app.route('/home')
def home():
	form = LoginForm(request.form)
	return render_template('home.html', form = form)

@app.route('/flappypong', methods=['POST', 'GET'])
@flask_login.login_required
def flappypong():
	
	if request.method == 'POST':
		if request.json != "get":
			userID = flask_login.current_user.get_id()
			u = db.query(User).filter_by(username=userID).first()
			userScores = u.flappy_scores
			if userScores == []:
				u.flappy_scores.append(FlappyPong(score = request.json))
				db.commit()
			elif userScores[0].score < request.json:
				db.delete(userScores[0])
				u.flappy_scores.append(FlappyPong(score = request.json))
				db.commit()
		flaps = db.query(FlappyPong).order_by(desc(FlappyPong.score)).limit(10).all()
		scores = {}
		for score in flaps:
			scores[score.user.username] = score.score
		return jsonify(scores);	
	return render_template('games/flappy_pong/flappy_pong.html')
#	return redirect(url_for('static', filename='games/flappy_pong/flappy_pong.html'))


@app.route('/gravitygolf', methods=['POST', 'GET'])
@flask_login.login_required
def gravitygolf():

	if request.method == 'POST':
		if request.json != "get":
			userID = flask_login.current_user.get_id()
			u = db.query(User).filter_by(username=userID).first()
			userScores = u.gravity_scores
			print(userScores)
			if userScores == []:
				u.gravity_scores.append(GravityGolf(score = request.json))
				db.commit()
			elif userScores[0].score > request.json:
				db.delete(userScores[0])
				u.gravity_scores.append(GravityGolf(score = request.json))
				db.commit()
		golfs = db.query(GravityGolf).order_by(desc(GravityGolf.score)).limit(10).all()
		scores = {}
		for score in golfs:
			scores[score.user.username] = score.score
		return jsonify(scores);	

	return render_template('games/GravityGolf/index.html')
	#return redirect(url_for('static', filename='games/GravityGolf/index.html'))


@app.route('/pacman', methods=['POST', 'GET'])
@flask_login.login_required
def pacman():

	if request.method == 'POST':
		if request.json != "get":
			userID = flask_login.current_user.get_id()
			u = db.query(User).filter_by(username=userID).first()
			userScores = u.pacman_scores
			if userScores == []:
				u.pacman_scores.append(Pacman(score = request.json))
				db.commit()
			elif userScores[0].score < request.json:
				db.delete(userScores[0])
				u.pacman_scores.append(Pacman(score = request.json))
				db.commit()
		pacs = db.query(Pacman).order_by(desc(Pacman.score)).limit(10).all()
		scores = {}
		for score in pacs:
			scores[score.user.username] = score.score
		return jsonify(scores);	


#	return render_template('games/pacman/index.html')
	return redirect(url_for('static', filename='javascript/pacman/index.html'))


@app.route('/lander', methods=['POST', 'GET'])
@flask_login.login_required
def lander():
	
	if request.method == 'POST':
		if request.json != "get":
			userID = flask_login.current_user.get_id()
			u = db.query(User).filter_by(username=userID).first()
			userScores = u.lander_scores
			if userScores == []:
				u.lander_scores.append(Lander(score = request.json))
				db.commit()
			elif userScores[0].score < request.json:
				db.delete(userScores[0])
				u.lander_scores.append(Lander(score = request.json))
				db.commit()
		lands = db.query(Lander).order_by(desc(Lander.score)).limit(10).all()
		scores = {}
		for score in lands:
			scores[score.user.username] = score.score
		return jsonify(scores);	
	return render_template('games/lander.html')
	

@app.route('/fifteen', methods=['POST', 'GET'])
@flask_login.login_required
def fifteen():

	if request.method == 'POST':
		if request.json != "get":
			userID = flask_login.current_user.get_id()
			u = db.query(User).filter_by(username=userID).first()
			userScores = u.fifteen_scores
			if userScores == []:
				u.fifteen_scores.append(Fifteen(score = request.json))
				db.commit()
			elif userScores[0].score > request.json:
				db.delete(userScores[0])
				u.fifteen_scores.append(Fifteen(score = request.json))
				db.commit()
		fifteen = db.query(Fifteen).order_by(desc(Fifteen.score)).limit(10).all()
		scores = {}
		for score in fifteen:
			scores[score.user.username] = score.score
		return jsonify(scores);	

	return render_template('games/fifteen/index.html')
#	return redirect(url_for('static', filename='games/fifteen/index.html'))



if __name__ == '__main__':
	app.run(debug='True',  host="0.0.0.0", port=8001)
