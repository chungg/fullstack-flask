import flask
from flask_security import auth_required, logout_user

from app.api import bp


@bp.get('/')
@auth_required()
def index():
    return flask.render_template("index.html")


@bp.get('/logout')
def logout():
    logout_user()
    return 'bye'


@bp.get('/health')
def healthcheck():
    return '¯\\_(ツ)_/¯'
