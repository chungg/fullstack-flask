from apiflask import APIFlask
from flask import url_for
from flask_admin import helpers as admin_helpers
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf import CSRFProtect
from loguru import logger

from app import admin, api
from app.config import cfg
from app.models import user as models
from app.storage.db import db


migrate = Migrate()
security = Security()
csrf = CSRFProtect()


def create_app(conf=cfg):
    app = APIFlask(__name__)
    app.config.from_object(conf)

    db.init_app(app)
    migrate.init_app(app, db)

    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    csrf.init_app(app)
    security.init_app(app, user_datastore)

    if conf.ENABLE_ADMIN:
        # set bootswatch theme: http://bootswatch.com/3/
        app.config['FLASK_ADMIN_SWATCH'] = 'journal'
        admin_ctx = admin.init_app(app, db)

    app.register_blueprint(api.bp)

    return app
