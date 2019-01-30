from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea

class ProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	full_name = StringField('Full name', validators=[DataRequired(), Length(4, 128)])
	date_joined = StringField('Date Joined', validators=[])
	receive_email = BooleanField('Subscriber to email notification', validators=[])
	update = SubmitField('update')

class AddChannelForm(FlaskForm):
	channel = StringField('Channel', validators=[DataRequired(), Length(4, 128)])
	description = StringField('Description', widget=TextArea())
	submit = SubmitField('Done')

class AddQuestionForm(FlaskForm):
	question = StringField('Question', validators=[DataRequired()])
	answer_page = StringField('Answer page')
	answer = StringField('Answer Description', widget=TextArea())
	submit = SubmitField('Done')