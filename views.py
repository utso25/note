from flask import ( 
	Blueprint, 
	redirect, 
	request, 
	render_template,
	url_for,
	flash
	)
from flask_login import (
	login_required, 
	login_user, 
	logout_user,
	current_user
	)
from .models import (
	User, 
	Note, 
	db
	)
from .forms import ( 
	RegistrationForm, 
	LoginForm
	)
from werkzeug.security import (
	generate_password_hash,
	check_password_hash
)



views = Blueprint("views", __name__)


@views.route('/')
def home():
	return redirect("/login")
	
@views.route('/register', 
methods=["GET", "POST"])
def register():
	form = RegistrationForm()
	if request.method == "POST":
		if form.validate_on_submit():
			email = form.email.data
			username = form.username.data
			password_d = form.password.data
			old_user = User.query.filter_by(email=email).first()
			if old_user:
				flash("Email is allready in use!")
			else:
				password = generate_password_hash(password_d)
				user = User(
				username=username, 
				email=email, 
				password=password
				)
				db.session.add(user)
				db.session.commit()
				login_user(user)
				return redirect(url_for("views.login"))
		return redirect(url_for("views.register"))
	return render_template("register.html",
	form=form)
	
@views.route('/login',
methods=["GET", "POST"])
def login():
	form = LoginForm()
	if request.method == "POST":
		if form.validate_on_submit():
			email = form.email.data
			password = form.password.data
			user = User.query.filter_by(email=email).first()
			if user:
				if check_password_hash(user.password, password):
					login_user(user)
					return redirect(url_for("views.note"))
				else:
					flash("Enter currect Password.")
			else:
				flash("Enter currect Email .")
	return render_template("login.html",
	form=form)

@views.route('/logout', 
methods=["GET", "POST"])
@login_required
def logout():
	if request.method == "POST":
		logout_user()
		return redirect(url_for("views.login"))
	return render_template("logout.html")

@views.route('/note', 
methods=["GET", "POST"])
@login_required
def note():
	notes = Note.query.filter_by(user=current_user.id)
	if request.method == "POST":
		note = request.form.get("note")
		if len(note) > 5 and len(note) < 5000:
			note_object = Note(note=note,
			user=current_user.id)
			db.session.add(note_object)
			db.session.commit()
			flash("Note Was Saved")
			return redirect(url_for("views.note"))
	return render_template("note.html",
	notes=notes)
	
@views.route('/note/delete/<id>', 
methods=["GET", "POST"])
@login_required
def delete(id):
	note = Note.query.filter_by(id=int(id)).first() or None
	if note:
		if request.method == "POST":
			if note.user == current_user.id:
				db.session.delete(note)
				db.session.commit()
				flash("Note Was Deleted!")
				return redirect(url_for("views.note"))
		return render_template("delete.html",
		note=note)
	return redirect(url_for('views.note'))
	
@views.route('/note/read/<id>', 
methods=["GET"])
@login_required
def read(id):
	note = Note.query.filter_by(id=int(id)).first() or None
	if note:
		if note.user == current_user.id:
			return render_template("read.html",
			note=note)
	return redirect(url_for('views.note'))
	
@views.route('/note/edit/<id>', 
methods = ["GET", "POST"])
@login_required
def edit(id):
	note = Note.query.filter_by(id=int(id)).first()
	if note and note.user == current_user.id:
		if request.method == "POST":
			note_u = request.form.get("note")
			note.note = note_u
			db.session.commit()
			return redirect(url_for("views.read",
			id=note.id))
		return render_template("edit.html", 
		note=note)
	return redirect(url_for("views.note"))