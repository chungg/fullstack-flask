from flask_security import logout_user
import sqlalchemy as sa

from app.api import bp
from app.storage.db import db


@bp.get('/logout')
def logout():
    logout_user()
    return 'bye'


@bp.get('/health')
def healthcheck():
    db.session.execute(sa.text('SELECT 1'))
    return '¯\\_(ツ)_/¯'
