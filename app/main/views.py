from app import db, moment
from app.main import main
from app.models import User, Channel, Question
from app.main.forms import ProfileForm, AddQuestionForm, AddChannelForm, PasswordChangeForm, DeleteAccountForm

from flask import render_template, current_app, request, redirect, url_for, jsonify, session, flash
from flask_login import current_user, login_required, logout_user
from sparkpost import SparkPost

import uuid
import bleach

# before request handler: redirect if not logged in .    
@main.before_request
def before_request():
	pass

# landing page 
@main.route('/')
def landing():
	return render_template('landing.html')


# homepage
@main.route('/home', methods=['POST', 'GET'])
@login_required
def home():
	form = AddChannelForm()

	if form.validate_on_submit():
		channel_key = uuid.uuid4().int & (1<<30)-1 # unique key for channel
		channel = Channel(key=channel_key, 
			created_by=current_user.uuid, 
			title=form.channel.data, 
			description = form.description.data) # create new channel instance 
		db.session.add(channel) # add instance into a session
		db.session.commit() # save to database

		#return redirect(url_for('main.channel', channel_key=channel_key))
		return redirect(url_for('main.home'))

	channel = db.session.query(Channel).filter(Channel.created_by == current_user.uuid).all() # get all channel records

	'''
	sp = SparkPost(current_app.config['SPARKPOST_KEY'])

	response = sp.transmissions.send(
		recipients=['toivo1996@gmail.com'],
		html='<p>Hello world</p>',
		from_email='password@kelaa.co',
		subject='Hello from python-sparkpost'
	)
	'''

	return render_template('home.html', form=form, channels=channel)

''' channel controller'''
@main.route('/c/<channel_key>')
@login_required
def channel(channel_key):
	channel = db.session.query(Channel).filter(Channel.key==channel_key).filter(Channel.created_by == current_user.uuid).first() # get active channel
	questions = db.session.query(Question).filter(Question.channel_key==channel_key).order_by(db.desc(Question.timestamp)).filter(Question.created_by==current_user.uuid).all() # all questions within this active session
	return render_template('/channel.html', channel=channel, questions=questions)

''' add question controller '''
@main.route('/c/<channel_key>/add', methods=['POST', 'GET'])
@login_required
def add_question(channel_key):
	form = AddQuestionForm()

	if form.validate_on_submit():
		question_key = uuid.uuid4().int & (1<<29)-1
		question = Question(key=question_key,
			created_by=current_user.uuid, 
			channel_key=channel_key,
			text=form.question.data,
			answer_page=form.answer_page.data,
			answer_text=form.answer.data) 
		db.session.add(question)
		db.session.commit()
		flash('Question added.', 'info')
		return redirect(url_for('main.add_question', channel_key=channel_key))

	channel = Channel.query.filter_by(key=channel_key).first()
		
	return render_template('add_question.html', form=form, channel=channel)

@main.route('/<username>/<tab>', methods=['POST', 'GET'])
def profile(username, tab):
	form = ProfileForm()
	securityform = PasswordChangeForm(prefix='a')
	deleteform = DeleteAccountForm(prefix='b')
	user = db.session.query(User).filter(User.username==username).first()

	if securityform.validate_on_submit():

		user.set_password(securityform.password.data)
		db.session.commit()

		flash('Password updated successfully', 'danger')
		return redirect(url_for('main.profile', username=user.username, tab=tab))
	
	if form.validate_on_submit():
		user.email = form.email.data
		user.userdetails.full_name = bleach.clean(form.full_name.data)
		user.username = form.username.data
		user.userdetails.receive_email = form.receive_email.data
		
		db.session.commit()
		flash('Profile updated successfully.', 'info')
		return redirect(url_for('main.profile', username=user.username, tab=tab))

	if deleteform.validate_on_submit():
		db.session.delete(user)
		db.session.commit()

		return redirect(url_for('auth.logout'))

	if user:
		form.email.data = user.email
		form.full_name.data = user.userdetails.full_name
		form.username.data = user.username
		form.receive_email.data = user.userdetails.receive_email

	return render_template('profile.html', form=form, user=user, securityform=securityform, deleteform=deleteform, active_page=tab)

''' routes envoked by javascript '''

@main.route('/update_channel', methods=['POST', 'GET'])
def update_channel():
	# initialize variables.
	key = request.form.get('key')
	title = request.form.get('title')
	description = request.form.get('description')

	channel = db.session.query(Channel).filter(Channel.key==key).first()

	if channel is not None:
		channel.title = title # update it's title
		channel.description = description #update it's description
		db.session.commit()

	flash('Updated successfully.', 'success')

	return 'a'

@main.route('/delete_channel', methods=['POST', 'GET'])
def delete_channel():

	key = request.form.get('key')
	channel = db.session.query(Channel).filter(Channel.key==key).first()
	db.session.delete(channel)
	db.session.commit()

	flash('Delete successfully', 'danger')

	return 'a'