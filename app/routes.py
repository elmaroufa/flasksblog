from flask import render_template, redirect, flash, url_for, request
from datetime import datetime
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LogimForm, RegisterForm, EditProfileForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@login_required
def index():
    user = {'username' : 'salyabbo'}
    return render_template('index.html', user=user)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('users.html',user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LogimForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        posts = Post.query.filter_by(id=user.id).all()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid user or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form, title = 'Sign in')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('COngratulation, you are new user')
        return redirect(url_for('login'))
    return render_template('register.html', title='Regiseter', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_see = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profil', methods=['GET', 'POST'])
@login_required
def edit_profil():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Change profil success')
        return redirect(url_for('edit_profil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data  = current_user.about_me
    return render_template('edit_profil.html', form=form, title='Edit profi')







