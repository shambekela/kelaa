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
	date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	avatar = db.Column(db.String(200))
	tokens = db.Column(db.Text)
	num_of_logins = db.Column(db.Integer, default=1)
	receiveEmail = db.Column(db.Boolean, default=True)
	password_hash = db.Column(db.String(255), nullable=True)
	confirmed = db.Column(db.Boolean, default=False)
	login_type = db.Column(db.Integer, nullable=False) # 0 - email and 1 - social login
	profile_type = db.Column(db.Integer, nullable=True) # 0 - student , 1 - Professional , 2- Hobbiest  

	# set getstarted modal seen
	def set_getStarted(self, seen):
		self.get_started = seen

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

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))