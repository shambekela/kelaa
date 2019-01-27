from . import main
from app import db, moment
from flask import render_template, current_app, request, redirect, url_for, jsonify, session
from flask_login import current_user, login_required, logout_user
from sparkpost import SparkPost
import tweepy

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
	t = []
	count = 1
	auth = tweepy.OAuthHandler('VTWhCr8Fhh5TngeDnHalrk8XV', 'M09bo6J0zDlXW5KIDmBb8dW7wk0GGNYyaHvDesBdNP6yk41Rmw')
	auth.set_access_token('2638191615-wXUK7gLIhIVbPeFoGNLFjRUZCeTHARxiFdn1OXG', 'ySSeKz4gLpUzQORaSeq7KlwHnBmAvPbvHjftAa1prypTP')
	api = tweepy.API(auth)
	for tweets in tweepy.Cursor(api.search,q="#success", result_type='mixed',count=15, lang="en", tweet_mode='extended').items():
		t.insert(0, (tweets.full_text))
		print('added')
		if count > 35:
			break
		count += 1

	return render_template('/channel.html', tweet=t, channel=channel_key)

@main.route('/c/<channel_key>/add/')
def add_question(channel_key):

	return render_template('add_question.html')