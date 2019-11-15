from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import flask_app, db
from app.models import User
from app.forms import LoginForm, SignupForm, EditProfileForm


@flask_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! you signed up successfully')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@flask_app.route('/')
@flask_app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@flask_app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Trekking was awesome'},
        {'author': user, 'body': 'Music is life'}
    ]
    return render_template('profile.html', title='Profile', user=user, posts=posts)


@flask_app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@flask_app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself...stupid')
        return redirect(url_for('profile', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following {}'.format(username))
    return redirect(url_for('profile', username=username))


@flask_app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself...stupid')
        return redirect(url_for('profile', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are no longer following {}'.format(username))
    return redirect(url_for('profile', username=username))


@flask_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@flask_app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
