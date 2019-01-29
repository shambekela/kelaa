from app import db, moment
from app.main import main
from app.models import User
from app.main.forms import ProfileForm, AddQuestionForm

from flask import render_template, current_app, request, redirect, url_for, jsonify, session
from flask_login import current_user, login_required, logout_user
from sparkpost import SparkPost

# before request handler: redirect if not logged in .    
@main.before_request
def before_request():
	pass

# landing page 
@main.route('/')
def landing():
	return 'Landing'


# homepage
@main.route('/home')
@login_required
def home():
	return render_template('home.html')

@main.route('/c/<channel_key>')
@login_required
def channel(channel_key):
	t = None
	return render_template('/channel.html', tweet=t, channel=channel_key)

''' add question controller '''
@main.route('/c/<channel_key>/add/')
def add_question(channel_key):
	form = AddQuestionForm()

	if form.validate_on_submit():
		pass
		
	return render_template('add_question.html', form=form)

@main.route('/profile/<username>')
def profile(username):
	form = ProfileForm()

	if form.validate_on_submit():
		pass

	user = User.query.filter_by(username=username).first()
	if user:
		form.email.data = user.email
		form.full_name.data = user.userdetails.full_name
		form.username.data = user.username
		form.date_joined.data = user.userdetails.date_joined

	return render_template('profile.html', form=form)