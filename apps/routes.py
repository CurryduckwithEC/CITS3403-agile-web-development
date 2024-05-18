import os

from flask import *
from flask_login import *
from werkzeug.utils import *

from apps import *
from apps.forms import *
from apps.models import *


@flaskApp.route('/')
def main():
    posts = Post.query.all()
    return render_template('main.html', posts=posts)


@flaskApp.context_processor
def inject_user():
    return dict(current_user=current_user)


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
                new_user = User(username=username, email=email, avatar='static/images/avatars/default_avatar.png')
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


@flaskApp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        tag_names = [name.strip() for name in form.tags.data.split(',')]
        for name in tag_names:
            if name:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('main'))
    return render_template('create_post.html', form=form)


@flaskApp.route('/tags/<int:tag_id>')
def tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag.html', tag=tag, posts=posts)


@flaskApp.route('/post/<int:post_id>')
def post(post_id):
    post = {
        "id": post_id,
        "title": "Dummy Post",
        "content": "This is a placeholder for a post."
    }
    return render_template('post.html', post=post)


@flaskApp.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


# Route for user profile
@flaskApp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


@flaskApp.route('/profile/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        abort(403)  # Forbidden if the current user is not the profile owner
    form = ProfileForm()
    if form.validate_on_submit():
        if form.avatar.data:
            filename = secure_filename(form.avatar.data.filename)
            avatar_dir = os.path.join(flaskApp.root_path, 'static/images/avatars')
            print("avatar_dir: " + avatar_dir)
            avatar_path = os.path.join(avatar_dir, filename).replace('\\', '/')
            print("avatar_path: " + avatar_path)
            form.avatar.data.save(avatar_path)
            user.avatar = os.path.join('images/avatars', filename).replace('\\', '/')
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user and existing_user != user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
        else:
            user.username = form.username.data
            user.email = form.email.data
            # Update password if provided
            if form.password.data and form.password.data == form.confirm_password.data:
                user.set_password(form.password.data)
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('profile', username=user.username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    return render_template('edit_profile.html', form=form)


@flaskApp.route('/check_username', methods=['POST'])
def check_username():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    return jsonify({'exists': user is not None})


@flaskApp.route('/check_email', methods=['POST'])
def check_email():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    return jsonify({'exists': user is not None})
