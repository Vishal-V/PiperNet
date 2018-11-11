from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .User import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.fetch_username(username.data)
		if user:
			raise ValidationError("This username is already taken. Please use a different one")

	def validate_email(self, email):
		user = User.fetch(email.data)
		if user:
			raise ValidationError("This email is already taken. Please use a different one")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
	name = StringField('name', validators=[DataRequired(), Length(min=2, max=15)])
	age = IntegerField('status', validators=[DataRequired()])
	status = StringField('status', validators=[DataRequired()])
	lives = StringField('lives', validators=[DataRequired()])
	place = StringField('place', validators=[DataRequired()])
	submit = SubmitField('Update')

	def check_username(self, username):
		user = User.fetch_username(username.data)
		if user:
			raise ValidationError("This username is already taken. Please use a different one")

	def check_email(self, email):
		user = User.fetch(email.data)
		if user:
			raise ValidationError("This email is already taken. Please use a different one")		