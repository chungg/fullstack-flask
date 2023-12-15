import flask
from flask_security import logout_user
import sqlalchemy as sa

from app.api import bp
from app.storage.db import db


@bp.get('/')
def index():
    return flask.render_template("index.html")


@bp.get('/analytics')
def analytics():
    return flask.render_template("analytics.html")


@bp.get('/yahoo')
def yahoo():
    return flask.render_template("yahoo.html")


@bp.get('/logout')
def logout():
    logout_user()
    return 'bye'


@bp.get('/health')
def healthcheck():
    db.session.execute(sa.text('SELECT 1'))
    return '¯\\_(ツ)_/¯'
