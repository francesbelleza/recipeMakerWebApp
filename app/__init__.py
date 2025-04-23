from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = app.config['LOGIN_VIEW']

from app.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



