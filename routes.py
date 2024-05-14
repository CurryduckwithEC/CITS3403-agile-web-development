from flask import render_template, request, redirect, url_for, flash
from apps import app, db
from apps.models import User

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login_register', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        form_type = request.form['formType']
        
        if form_type == 'login':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:
               
                flash('Logged in successfully.', 'success')
                return redirect(url_for('main'))
            else:
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('login_register'))
        
        elif form_type == 'register':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirmPassword']

            if password != confirm_password:
                flash('Passwords do not match', 'danger')
                return redirect(url_for('login_register'))

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists', 'danger')
                return redirect(url_for('login_register'))

            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login_register'))

    return render_template('login_register.html')

@app.route('/post')
def post():
    return render_template('post.html')
