from flask import *
from flask_login import login_user, logout_user, login_required

from apps import *
from apps.forms import *
from apps.models import *


@flaskApp.route('/')
def main():
    return render_template('main.html')


@flaskApp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)


@flaskApp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@flaskApp.route('/post')
def post():
    return render_template('post.html')


@flaskApp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the username or email already exists in the database
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
            return render_template('registration.html', form=form)

        # Create a new user instance
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    else:
        redirect(url_for('registration'))
    return render_template('registration.html', form=form)
