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


@flaskApp.route('/check_email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email', '')
    user = User.query.filter_by(email=email).first()
    return jsonify({'exists': user is not None})


@flaskApp.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data.get('username', '')
    user = User.query.filter_by(username=username).first()
    return jsonify({'exists': user is not None})


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


@flaskApp.route('/profile/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        abort(403)  # Forbidden if the current user is not the profile owner
    form = ProfileForm()
    print("Value of form.validate_on_submit: " + str(form.validate_on_submit()))
    if form.validate_on_submit():
        # Check for username uniqueness.
        if User.query.filter(User.username == form.username.data, User.id != user.id).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('edit_profile.html', form=form, user=user)

        if User.query.filter(User.email == form.email.data, User.id != user.id).first():
            flash('Email already exists. Please choose a different one.', 'danger')
            return render_template('edit_profile.html', form=form, user=user)

        if form.avatar.data:
            filename = secure_filename(form.avatar.data.filename)
            avatar_dir = os.path.join(flaskApp.root_path, 'static/images/avatars')
            avatar_path = os.path.join(avatar_dir, filename).replace('\\', '/')
            form.avatar.data.save(avatar_path)
            user.avatar = os.path.join('images/avatars', filename).replace('\\', '/')

        user.username = form.username.data
        user.email = form.email.data

        # Update password if provided
        if form.password.data and form.password.data == form.confirm_password.data:
            user.set_password(form.password.data)

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=user.username, user=user))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    return render_template('edit_profile.html', form=form, user=user)


@flaskApp.route('/get_trending_posts')
def get_trending_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    posts_query = Post.query.order_by(Post.created_at.desc())
    posts_paginated = posts_query.paginate(page=page, per_page=per_page, error_out=False)
    posts = [{
        'id': post.id,
        'title': post.title,
        'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
        'author': post.author.username,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M'),
        'last_reply_at': post.last_reply_at.strftime('%Y-%m-%d %H:%M') if post.last_reply_at else 'No replies yet',
        'liked': post.likes,
        'comments_count': len(post.comments)
    } for post in posts_paginated.items]

    return jsonify(posts=posts, has_next=posts_paginated.has_next)


@flaskApp.context_processor
def inject_user():
    return dict(current_user=current_user)


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


@flaskApp.route('/post/<int:post_id>')
def post(post_id):
    post = {
        "id": post_id,
        "title": "Dummy Post",
        "content": "This is a placeholder for a post."
    }
    return render_template('post.html', post=post)


@flaskApp.route('/post_for_answer')
def post_for_answer():
    return render_template('post_for_answer.html')


@flaskApp.route('/post_for_service')
def post_for_service():
    return render_template('post_for_service.html')


# Route for user profile
@flaskApp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


@flaskApp.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@flaskApp.route('/tags/<int:tag_id>')
def tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag.html', tag=tag, posts=posts)
