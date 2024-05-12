from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from apps.config import Config

flaskApp = Flask(__name__)
flaskApp.config.from_object(Config)
db = SQLAlchemy(flaskApp)
migrate = Migrate(flaskApp, db)
login = LoginManager(flaskApp)
login.login_view = 'login'

from .models import User
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from apps import routes
from apps import models
