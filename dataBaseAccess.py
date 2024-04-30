from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class jobPostings(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=False, nullable=False)
    jobPay = db.Column(db.Integer, unique=False, nullable=False)
    body = db.Column(db.String(600), unique=False, nullable=False)