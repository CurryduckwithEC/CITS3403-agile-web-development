from flask import *
from flask_login import *
from werkzeug.utils import *

from apps import *
from apps.forms import *
from apps.models import *


# The main page.
@flaskApp.route('/')
def main():
    posts = Post.query.all()
    return render_template('main.html', posts=posts)


# Adding a comment to a post.
@flaskApp.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return redirect(url_for('post', post_id=post.id))


# Ajax for email checking when editing profile.
@flaskApp.route('/check_email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email', '')
    user = User.query.filter_by(email=email).first()
    return jsonify({'exists': user is not None})


# Ajax for username checking when editing profile.
@flaskApp.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data.get('username', '')
    user = User.query.filter_by(username=username).first()
    return jsonify({'exists': user is not None})


# The page for creating a post.
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


# The page for editing profile.
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


# Post feed in the main page.
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
        'liked': post.is_liked_by_current_user(current_user),
        'comments_count': len(post.comments)
    } for post in posts_paginated.items]

    return jsonify(posts=posts, has_next=posts_paginated.has_next)


@flaskApp.context_processor
def inject_user():
    return dict(current_user=current_user)


# The login page.
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

# The functionality of logging out.
@flaskApp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# The post page with comments.
@flaskApp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data, author=current_user, post=post)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added!', 'success')
            return redirect(url_for('post', post_id=post.id))
        else:
            flash('You need to log in to add a comment.', 'danger')
            return redirect(url_for('login'))
    return render_template('post.html', post=post, form=form)


# The profile page.
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


# The search functionality.
@flaskApp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        posts = Post.query.filter((Post.title.ilike(f'%{query}%')) | (Post.content.ilike(f'%{query}%'))).all()
        comments = Comment.query.filter(Comment.content.ilike(f'%{query}%')).all()
        users = User.query.filter(User.username.ilike(f'%{query}%')).all()
        tags = Tag.query.filter(Tag.name.ilike(f'%{query}%')).all()

        results = {
            'posts': [{'id': post.id, 'title': post.title, 'content': post.content, 'author': post.author.username, 'tags': [tag.name for tag in post.tags]} for post in posts],
            'comments': [{'content': comment.content, 'author': comment.author.username} for comment in comments],
            'users': [{'username': user.username} for user in users],
            'tags': [{'name': tag.name} for tag in tags]
        }
        return jsonify(results)
    return jsonify({'posts': [], 'comments': [], 'users': []})


@flaskApp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        likes_count = Like.query.filter_by(post_id=post_id).count()
        return jsonify({'status': 'success', 'likes': likes_count, 'liked': False})
    else:
        new_like = Like(post_id=post_id, user_id=current_user.id)
        db.session.add(new_like)
        db.session.commit()
        likes_count = Like.query.filter_by(post_id=post_id).count()
        return jsonify({'status': 'success', 'likes': likes_count, 'liked': True})
