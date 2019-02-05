from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets import TextArea
from wtforms import ValidationError
from flask_login import current_user

class ProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	full_name = StringField('Full name')
	receive_email = BooleanField('Subscriber to email notification')
	update = SubmitField('update')

class PasswordChangeForm(FlaskForm):
	oldpassword = PasswordField('Old Password', validators=[DataRequired(), Length(min=6)])
	password = PasswordField('New Password', validators=[DataRequired(), Length(min=6),  EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('Confirm password', validators=[DataRequired(), Length(min=6)])
	submit = SubmitField('Update Password')

	def validate_oldpassword(self, oldpassword):
		if not current_user.check_password(oldpassword.data):
			raise ValidationError('Please enter your current password.')

class AddChannelForm(FlaskForm):
	channel = StringField('Channel', validators=[DataRequired(), Length(4, 128)])
	description = StringField('Description', widget=TextArea())
	submit = SubmitField('Done')

class AddQuestionForm(FlaskForm):
	question = StringField('Question', validators=[DataRequired()])
	answer_page = StringField('Answer page')
	answer = StringField('Answer Description', widget=TextArea())
	submit = SubmitField('Done')

class DeleteAccountForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Delete')

	def validate_password(self, password):
		if not current_user.check_password(password.data):
			raise ValidationError('Incorrect password.')