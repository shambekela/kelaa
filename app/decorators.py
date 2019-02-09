from functools import wraps
from flask import redirect, url_for

def user_loggedin(user):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if user.is_authenticated:
				return redirect(url_for('main.home'))
			return f(*args, **kwargs)
		return decorated_function
	return decorator