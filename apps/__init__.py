from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from apps.config import Config

# Set up configurations.

flaskApp = Flask(__name__)
flaskApp.config.from_object(Config)
db = SQLAlchemy(flaskApp)
migrate = Migrate(flaskApp, db)
login = LoginManager()
login.init_app(flaskApp)
login.login_view = 'login'

ckeditor = CKEditor(flaskApp)
flaskApp.config['CKEDITOR_PKG_TYPE'] = 'full'
flaskApp.config['CKEDITOR_HEIGHT'] = 400

from .models import User


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from apps import routes
from apps import models
