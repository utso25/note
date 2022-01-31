from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


website = Flask(__name__)
website.config['SECRET_KEY'] = "#sAcReTTi"
website.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///databse.db"

db = SQLAlchemy(website)

from .models import User
login_manager = LoginManager(website)
login_manager.init_app(website)
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from .views import views
website.register_blueprint(views, 
url_prefix="")

def get_website():
	return website
	
@website.errorhandler(401)
def _401(e):
    return render_template("401.html")
    
@website.errorhandler(404)
def _404(e):
    return render_template("404.html")
    
@website.errorhandler(405)
def _405(e):
    return render_template("405.html")
    
@website.errorhandler(500)
def _500(e):
    return render_template("500.html")