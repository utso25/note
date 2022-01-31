from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(
	db.Integer(), primary_key = True)
	email = db.Column(
	db.String(50), nullable = False, unique=True)
	username = db.Column(
	db.String(25), nullable = False)
	password = db.Column(
	db.String(50), nullable = False)
	
	def __str__(self):
		return self.username

class Note(db.Model):
	id = db.Column(
	db.Integer(), primary_key = True)
	note = db.Column(
	db.String(5000), nullable = False)
	user = db.Column(db.Integer())
	
	def __str__(self):
		return self.note[:15]