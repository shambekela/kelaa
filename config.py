import os
from whoosh.analysis import StemmingAnalyzer

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Auth:
	CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
	CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
	REDIRECT_URI = 'http://localhost:5000/gCallback'
	AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
	TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
	USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
	SCOPE = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
	
class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'afafd6a5f65a6f5a65df6a5f6af65daf84df23sfa6d5fa'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = 'postgres://mqnnybvzsoecdu:20e016e0ea332c909ce251bcbb5e4ff86ca3b5ee07b30c204db4f48a74836e16@ec2-54-235-159-101.compute-1.amazonaws.com:5432/d6q284ahkijbqd'
	#'mysql+pymysql://root@localhost/kelaa'
	SPARKPOST_KEY = os.environ.get('SPARKPOST_KEY') 
	SPARKPOST_CONTACT_EMAIL = os.environ.get('SPARKPOST_EMAIL') or 'no-reply@kelaa.co'
	WHOOSH_ANALYZER = StemmingAnalyzer()
	WHOOSH_BASE = 'whoosh'

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SSL_REDIRECT = False

class TestingConfig(Config):
	pass

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

	@classmethod
	def init_app(cls, app):
		Config.init_app(app)
	
class HerokuConfig(ProductionConfig):
	SSL_REDIRECT = True if os.environ.get('DYNO') else False

	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)

		# handle reverse proxy server headers
		from werkzeug.contrib.fixers import ProxyFix
		app.wsgi_app = ProxyFix(app.wsgi_app)

		# log to stderr
		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)


config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'testing': TestingConfig,
	'heroku': HerokuConfig,

	'default': DevelopmentConfig
}