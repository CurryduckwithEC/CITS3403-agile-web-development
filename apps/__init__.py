from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.urandom(24)

# Create an instance of SQLAlchemy called db.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from apps import routes
from apps import models


