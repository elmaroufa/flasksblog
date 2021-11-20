from flask import render_template

from app import app


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