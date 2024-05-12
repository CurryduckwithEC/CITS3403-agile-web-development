from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from apps import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    hashedPassword = db.Column(db.String(30), nullable=False)

    def set_password(self, password):
        self.hashedPassword = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashedPassword, password)

    def __repr__(self):
        return f'<User {self.username}>'
