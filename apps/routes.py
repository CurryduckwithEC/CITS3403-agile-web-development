from flask import *
from flask_login import login_user, logout_user, login_required

from apps import *
from apps.forms import *
from apps.models import *


@flaskApp.route('/')
def main():
    posts = [
        {'id': 1, 'title': 'First Post',
         'content': 'This is the content of the first post. Lorem ipsum dolor sit amet...', 'liked': False},
        {'id': 2, 'title': 'Second Post',
         'content': 'Here goes the content of the second post, quite longer than the first one...', 'liked': True}
    ]
    return render_template('main.html', posts=posts)


@flaskApp.route('/post_for_answer')
def post_for_answer():
    return render_template('post_for_answer.html')


@flaskApp.route('/post_for_service')
def post_for_service():
    return render_template('post_for_service.html')


@flaskApp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    registration_form = UserRegistrationForm()
    if request.method == 'POST':
        print("POST request received")  # Debug print
        print(request.form)  # Debug print

        form_type = request.form.get('form_type')
        print(form_type)
        if form_type == 'login' and login_form.validate_on_submit():
            print("Login form submitted")  # Debug print
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('main'))
            else:
                flash('Invalid email or password.', 'danger')
        elif form_type == 'register' and registration_form.validate_on_submit():
            print("Registration form submitted and validated")  # Debug print
            username = registration_form.username.data
            email = registration_form.email.data
            password = registration_form.password.data
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                flash('Username or email already exists. Please choose a different one.', 'danger')
            else:
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('login'))
        else:
            print("Form validation failed")  # Debug print
            if form_type == 'register':
                print(registration_form.errors)  # Debug print
    return render_template('login.html', login_form=login_form, registration_form=registration_form)


@flaskApp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@flaskApp.route('/post')
def post():
    return render_template('post.html')
