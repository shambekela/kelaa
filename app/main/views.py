from . import main
from app import db, moment
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
	return str(current_user.email)