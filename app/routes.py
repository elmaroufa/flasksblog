from flask import render_template, redirect, flash, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LogimForm, RegisterForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@login_required
def index():
    user = {'username' : 'salyabbo'}
    return render_template('index.html', user=user)


@app.route('/user/<name>')
def user(name):
    return render_template('users.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
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







