from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


class UserRegistrationForm(FlaskForm):
    form_type = HiddenField(default='register')
    username = StringField("Username:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password:", validators=[DataRequired(), EqualTo('password',
                                                                                             message='Passwords must match')])
    submitButton = SubmitField("Submit")
    resetButton = SubmitField("Reset")


class LoginForm(FlaskForm):
    form_type = HiddenField(default='login')
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    loginButton = SubmitField("Login")
