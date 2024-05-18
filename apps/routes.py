from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from apps import db
from apps.forms import LoginForm, UserRegistrationForm, PostForm
from apps.models import User, Post

flaskApp = Blueprint('flaskApp', __name__)

@flaskApp.route('/')
def main():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('main.html', posts=posts)

@flaskApp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('flaskApp.main'))
    return render_template('create_post.html', form=form)

@flaskApp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    registration_form = UserRegistrationForm()
    if request.method == 'GET':
        return render_template('login.html', login_form=login_form, registration_form=registration_form)

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('flaskApp.main'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', login_form=login_form, registration_form=registration_form)

@flaskApp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('flaskApp.login'))

@flaskApp.route('/registration', methods=['GET', 'POST'])
def registration():
    login_form = LoginForm()
    registration_form = UserRegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        email = registration_form.email.data
        password = registration_form.password.data

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
            return render_template('login.html', registration_form=registration_form, login_form=login_form)

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('flaskApp.login'))
    return render_template('login.html', registration_form=registration_form, login_form=login_form)

@flaskApp.route('/post_for_answer')
def post_for_answer():
    return render_template('post_for_answer.html')

@flaskApp.route('/post_for_service')
def post_for_service():
    return render_template('post_for_service.html')

@flaskApp.route('/submit_service', methods=['POST'])
def submit_service():
    title = request.form.get('title')
    description = request.form.get('description')
    flash('Service offered successfully!', 'success')
    return redirect(url_for('flaskApp.main'))

@flaskApp.route('/submit_answer', methods=['POST'])
def submit_answer():
    title = request.form.get('title')
    content = request.form.get('content')
    flash('Answer posted successfully!', 'success')
    return redirect(url_for('flaskApp.main'))

@flaskApp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
