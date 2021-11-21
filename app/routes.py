from flask import render_template, redirect, flash, url_for
from app import app
from app.forms import LogimForm

@app.route('/')
def index():
    user = {'username' : 'salyabbo'}
    return render_template('base.html', user=user)


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
    form = LogimForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, 
        form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form, title = 'Sign in')
