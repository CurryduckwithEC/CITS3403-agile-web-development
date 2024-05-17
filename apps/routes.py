from flask import *
from flask_login import login_user, logout_user, login_required

from apps import *
from apps.forms import *
from apps.models import *

@flaskApp.route('/')
def main():
    posts = [
        {'id': 1, 'title': 'First Post', 'content': 'This is the content of the first post. Lorem ipsum dolor sit amet...', 'liked': False},
        {'id': 2, 'title': 'Second Post', 'content': 'Here goes the content of the second post, quite longer than the first one...', 'liked': True}
    ]
    return render_template('main.html', posts=posts)



@flaskApp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    registration_form = UserRegistrationForm()
    if request.method == 'GET':
        return render_template('login.html', login_form =login_form, registration_form=registration_form)

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', login_form =login_form,registration_form=registration_form)

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
    login_form = LoginForm()
    registration_form = UserRegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        email = registration_form.email.data
        password = registration_form.password.data

        # Check if the username or email already exists in the database
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
            return render_template('registration.html', registration_form=registration_form, login_form=login_form)

        # Create a new user instance
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
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
    # Handle the form submission logic here
    flash('Service offered successfully!', 'success')
    return redirect(url_for('main'))

@flaskApp.route('/submit_answer', methods=['POST'])
def submit_answer():
    title = request.form.get('title')
    content = request.form.get('content')
    # Handle the form submission logic here
    flash('Answer posted successfully!', 'success')
    return redirect(url_for('main'))

@flaskApp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)