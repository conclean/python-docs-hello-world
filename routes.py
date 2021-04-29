from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from forms import LoginForm, SignupForm, ProfileForm
from models import User, Post, Profile
from config import Config
import os


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Vivek'}
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.username == form.username.data).first()
        if not user_in_db:
            flash('No user found with username: {}'.format(form.username.data))
            return redirect(url_for('login'))
        if check_password_hash(user_in_db.password_hash, form.password.data):
            flash('Login success!')
            session["USERNAME"] = user_in_db.username
            return redirect(url_for('profile'))
        flash('Incorrect Password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))
        passw_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
        db.session.add(user)
        db.session.commit()
        flash('User registered with username:{}'.format(form.username.data))
        session["USERNAME"] = user.username
        print(session)
        return redirect(url_for('profile'))
    return render_template('signup.html', title='Register a new user', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            cv_dir = Config.CV_UPLOAD_DIR
            file_obj = form.cv.data
            cv_filename = session.get("USERNAME") + '_CV.pdf'
            file_obj.save(os.path.join(cv_dir, cv_filename))
            flash('CV uploaded and saved')
            return redirect(url_for('index'))
        return render_template('profile.html', title='Add/Modify your profile', form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('login'))
