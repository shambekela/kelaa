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
	question = db.relationship('Question', backref='question', lazy=True)
	userdetails = db.relationship('UserDetail', backref='details', uselist=False, cascade="all, delete", lazy=True)

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

		self.userdetails.email_confirmed = True
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

		if user is None:
			return False
		user.set_password(new_password)
		db.session.add(user)
		db.session.commit()
		return True

class UserDetail(db.Model):
	__tablename__ = 'user_detail'
	id = db.Column(db.Integer, primary_key=True)
	user_uuid = db.Column(db.Integer, db.ForeignKey('user.uuid', ondelete="CASCADE"))
	receive_email = db.Column(db.Boolean, default=True)
	email_confirmed = db.Column(db.Boolean, default=False)
	login_type = db.Column(db.Integer, default=1) # 1 - email, 2 - google, 3 - twitter
	'''
	user_type = db.Column(db.Integer, db.ForeignKey('user_type.id'))
	'''
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
	questions = db.relationship('Question', backref='quest', cascade="all, delete",lazy=True)

	def question_count(self):
		que = db.session.query(Question).filter(Question.channel_key == self.key).count()
		return que

	def last_added(self):
		date = db.session.query(Question.timestamp).filter(Question.channel_key == self.key).order_by(db.desc(Question.timestamp)).first()
		return date

class Question(db.Model):
	__searchable__ = ['text', 'answer_text']

	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.Integer, unique=True)
	channel_key = db.Column(db.Integer, db.ForeignKey('channel.key', ondelete="CASCADE"))
	created_by = db.Column(db.Integer, db.ForeignKey('user.uuid'))
	text = db.Column(db.String(255), nullable=False)
	answer_page = db.Column(db.String(128))
	answer_text = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	favourite = db.Column(db.Boolean, default=False)
	activities = db.relationship('Activity', backref='question', lazy=True)

class Tracker(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	user_uuid = db.Column(db.Integer, db.ForeignKey('user.uuid'))

class Activity(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	activity_id = db.Column(db.Integer, unique=True)
	user_uuid = db.Column(db.Integer, db.ForeignKey('user.uuid'))
	channel_id = db.Column(db.Integer, db.ForeignKey('channel.key'))
	current_question = db.Column(db.Integer, db.ForeignKey('question.key'))
	started_date = db.Column(db.Integer, default=datetime.utcnow)
	in_progress = db.Column(db.Boolean, default=True)

'''
class LoginType(db.Model):
	__tablename__ = 'login_type'
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(128), nullable=False) # 1 - email, 2 - google, 3 - twitter
	users = db.relationship('UserDetail', backref='logintype', lazy=True)

class UserType(db.Model):
	__tablename__ = 'user_type'
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(128), nullable=False) # google, email, twitter
	users = db.relationship('UserDetail', backref='logintype', lazy=True)
'''
@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))
