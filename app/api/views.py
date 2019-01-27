from . import api 
from flask import render_template, redirect, url_for, request, session
from flask_login import login_user, login_required, current_user, logout_user
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
from config import Auth
from app import db
from app.models import User, UserDetail
import json, uuid, sys, string

def get_google_auth(state=None, token=None):
	if token:
		return OAuth2Session(Auth.CLIENT_ID, token=token)
	if state:
		return OAuth2Session(Auth.CLIENT_ID, state=state, redirect_uri=Auth.REDIRECT_URI, scope=Auth.SCOPE)
	oauth = OAuth2Session(Auth.CLIENT_ID, redirect_uri=Auth.REDIRECT_URI, scope=Auth.SCOPE)
	return oauth

@api.route('/google_login', methods=['POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	
	google = get_google_auth()
	auth_url, state = google.authorization_url(Auth.AUTH_URI, access_type='offline')
	session['oauth_state'] = state
	return redirect(auth_url)

@api.route('/logout')
@login_required
def logout():
	logout_user()
	session.clear()
	return redirect(url_for('auth.login'))

@api.route('/gCallback')
def callback():
	if current_user is not None and current_user.is_authenticated:
		return redirect(url_for('main.home'))

	if 'error' in request.args:
		if request.args.get('error') == 'access_denied':
			return 'You are denied access'

		return 'Error encountered.'

	if 'code' not in request.args and 'state' not in request.args:
		return redirect(url_for('main.home'))

	else:
		google = get_google_auth(state=session['oauth_state'])

		try:
			token = google.fetch_token(Auth.TOKEN_URI, client_secret=Auth.CLIENT_SECRET, authorization_response=request.url)
		except HTTPError:
			return 'HTTPError Occurred'

		google = get_google_auth(token=token)
		resp = google.get(Auth.USER_INFO)

		if resp.status_code==200:
			user_data = resp.json()
			print(user_data)
			email = user_data['email']
			user = User.query.filter_by(email=email).first()
			detail = None
			if user is None:
				uud = (uuid.uuid4().int & (1<<29)-1)
				user = User()
				detail = UserDetail()
				user.email = email
				user.uuid = uud
				detail.user_uuid = uud
			else:
				detail = UserDetail.query.filter_by(user_uuid = user.uuid).first()
				
			user.username = user_data['family_name']
			
			detail.tokens = json.dumps(token)
			detail.avatar = user_data['picture']
			detail.full_name = string.capwords(user_data['given_name'] + ' ' + user_data['family_name'])
			detail.email_confirmed = True 
			detail.login_type = 2

			db.session.add(user)
			db.session.add(detail)
			db.session.commit()
			login_user(user, remember=True)
			return redirect(url_for('main.home'))
		return 'Could not fetch data'