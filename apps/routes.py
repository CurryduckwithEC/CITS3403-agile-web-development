from flask import render_template, request, redirect, url_for, flash

from apps import flaskApp, db
from apps.models import User


@flaskApp.route('/')
def main():
    return render_template('main.html')


@flaskApp.route('/login')
def login():
    return render_template('login.html')


@flaskApp.route('/post')
def post():
    return render_template('post.html')


@flaskApp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        # Need to delete
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('registration.html')
