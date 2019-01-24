from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


# tables stores user account data and related info.
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	uuid = db.Column(db.Integer, unique=True ,index=True)
	username = db.Column(db.String(255), unique=True, nullable=False)
	email = db.Column(db.String(255), unique=True)
	password_hash = db.Column(db.String(255), nullable=True)
	channels = db.relationship('Channel', backref='creator', lazy=True)
	trackers = db.relationship('Tracker', backref='user', lazy=True) 

	# set getstarted modal seen
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.uuid}).decode('utf-8')

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except Exception as e:
			return False

		if data.get('confirm') != self.uuid:
			return False

		self.confirmed = True
		db.session.add(self)
		return True

	def generate_reset_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.uuid}).decode('utf-8')

	@staticmethod
	def reset_password(token, new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		user = db.session.query(User).filter(User.uuid==data.get('reset')).first()
		print(user)
		if user is None:
			return False
		user.set_password(new_password)
		db.session.add(user)
		db.session.commit()
		return True

class UserDetails(db.Model):
	__tablename__ = 'user_detail'
	id = db.Column(db.Integer, auto_increment=True)
	user_uuid = db.Column(db.Integer, db.ForeignKey('user.uuid', ondelete="CASCADE"))
	receive_email = db.Column(db.Boolean, default=True)
	email_confirmed = db.Column(db.Boolean, default=False)
	login_type = db.Column(db.Integer, db.ForeignKey('login_type.id'))
	user_type = db.Column(db.Integer, db.ForeignKey('user_type.id'))
	date_joined = db.Column(db.DateTime, default=datetime.utcnow)
	full_name = db.Column(db.String(255), index=True)
	avatar = db.Column(db.String(200))
	tokens = db.Column(db.Text)

class Channel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.Integer, unique=True, index=True)
	created_on = db.Column(db.DateTime, default=datetime.utcnow)
	created_by = db.Column(db.Integer, db.ForeignKey('user.uuid'))
	title = db.Column(db.String(255), nullable=False, index=True)
	description = db.Column(db.Text, nullable=True)
	questions = db.relationship('Question', backref='question', cascade="all, delete",lazy=True)

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.String(128), unique=True)
	channel_key = db.Column(db.Integer, db.ForeignKey('channel.key', ondelete="CASCADE"))
	text = db.Column(db.String(255), nullable=False)
	answer_page = db.Column(db.String(128))
	answer_text = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	favourite = db.Column(db.Boolean, default=False)

class Tracker(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	user_uuid = db.Column(db.Integer, db.ForeignKey('user.uuid'))

class Activity(db.Model):
	id = 


class LoginType(db.Model):
	__tablename__ = 'login_type'
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(128), nullable=False) # google, email, twitter
	users = db.relationship('UserDetails', backref='logintype', lazy=True)	


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))