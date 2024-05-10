from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from apps.config import Config

flaskApp = Flask(__name__)
flaskApp.config.from_object(Config)

# Create an instance of SQLAlchemy called db.
db = SQLAlchemy(flaskApp)
migrate = Migrate(flaskApp, db)

from apps import routes
from apps import models
