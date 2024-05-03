from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class jobPostings(db.Model):
    user_id = db.Column(db.Integer, foreign_key=True)
    title = db.Column(db.String(32), unique=False, nullable=False)
    jobPay = db.Column(db.Integer, unique=False, nullable=False)
    body = db.Column(db.String(600), unique=False, nullable=False)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))