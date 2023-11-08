import flask
from flask_security import auth_required, logout_user

from app.api import bp


@bp.route('/')
@auth_required()
def index():
    return flask.render_template("index.html")


@bp.route('/logout')
def logout():
    logout_user()
    return 'bye'


@bp.route('/users')
def get_user():
    return 'asdf'
