from flask import Flask, render_template, request, redirect, url_for
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

app = Flask(__name__)
#os.urandom(24)
app.secret_key = '\x1fy\xb0[\x85\xf2\xe5\xd4\x94\x06F\xd9\x1dd\x93\x14\xde\xb1\x12H\xa2\x15V\x90'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

Bootstrap(app)

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
#	if type(form).__name__ == RegistrationForm and exists != None:
#		field.errors.append('Username already exists')
#		return False

	if exists == None:
		field.errors.append('Username does not exist')
		return False


class LoginForm(Form):
	username = StringField('Username', [validators.Length(min=3, max=25), Username_check])
	password = PasswordField('Password', validators=[DataRequired()])
	
	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False
		
		u = db.query(User).filter_by(username=self.username.data).first()
		if u.verify_password(self.password.data.encode()) == False:
			self.password.errors.append('Invalid password')
			return False
		
		return True

class RegistrationForm(Form):
	username = StringField('Username', [validators.Length(min=3, max=25)])
	password = PasswordField('New Password', [validators.Length(min=3, max=72), validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')

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
	username = request.form.get('username')
	u = db.query(User).filter_by(username=username)
	exists = u.scalar()
	if exists == None:
		return None
	print('test')
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


@app.route('/register', methods=['Get', 'POST'])
def register():
	if flask_login.current_user.is_authenticated:
		return redirect(url_for('home'))
	next = get_redirect_target()
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

	return render_template('register.html', form = form, next=next)



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

@app.route('/flappypong')
@flask_login.login_required
def flappypong():
	return redirect(url_for('static', filename='games/flappy_pong/flappy_pong.html'))


@app.route('/gravitygolf')
@flask_login.login_required
def gravitygolf():
	return redirect(url_for('static', filename='games/GravityGolf/index.html'))


@app.route('/pacman')
@flask_login.login_required
def pacman():
	return redirect(url_for('static', filename='games/Pacman/index.html'))


@app.route('/lander')
@flask_login.login_required
def lander():
	return redirect(url_for('static', filename='games/lander.html'))

@app.route('/fifteen')
@flask_login.login_required
def fifteen():
	return redirect(url_for('static', filename='games/fifteen/index.html'))









if __name__ == '__main__':
	app.run(debug='True',  host="0.0.0.0", port=8001)
