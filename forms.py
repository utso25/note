from flask_wtf import FlaskForm
from wtforms import (
	StringField,
	PasswordField
	)
from wtforms.validators import (
	Email,
	Length,
	EqualTo
	)

class RegistrationForm(FlaskForm):
	email = StringField("Email Adress",
	validators=[Length(min=7, max=50)])
	username = StringField("Username",
	validators=[Length(min=3, max=25)])
	password = PasswordField("Password",
	validators=[Length(min=7, max=50)])
	password_c = PasswordField("Password",
	validators=[Length(min=7, max=50), 
	EqualTo('password')])
	
class LoginForm(FlaskForm):
	email = StringField("Email Adress",
	validators=[Length(min=7, max=50)])
	password = PasswordField("Password",
	validators=[Length(min=7, max=50)])