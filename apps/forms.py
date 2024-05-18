from flask_wtf import FlaskForm
from flask_wtf.file import *
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


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tags = StringField('Tags (comma separated)')
    submit = SubmitField('Create Post')


class ProfileForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    avatar = FileField("Upload Avatar", validators=[
        FileAllowed(['jpg', 'png'], 'Images only!'),
        FileSize(max_size=5 * 1024 * 1024)  # 5 MB limit
    ])
    password = PasswordField("New Password", validators=[Optional()])
    confirm_password = PasswordField("Confirm New Password",
                                     validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Update Profile")
