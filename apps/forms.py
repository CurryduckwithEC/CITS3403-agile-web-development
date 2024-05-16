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

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == self.username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')
