from flask import *

from apps import flaskApp, db
from apps.forms import *
from apps.models import *


@flaskApp.route('/')
def main():
    return render_template('main.html')


@flaskApp.route('/login')
def login():
    return render_template('login.html')


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
            return redirect(url_for('registration'))

        # Create a new user instance
        new_user = User(username=username, email=email, password=password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)
