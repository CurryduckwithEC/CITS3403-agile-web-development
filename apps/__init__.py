from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from apps.config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'flaskApp.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from apps.routes import flaskApp as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from .models import User
from . import routes, models
