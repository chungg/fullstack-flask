from apiflask import APIFlask
from flask_security import SQLAlchemyUserDatastore
from loguru import logger

from app import admin, api
from app.config import cfg
from app.extensions import csrf, migrate, security
from app.models import auth as models
from app.storage.db import db


def create_app(conf=cfg):
    logger.info('starting app...')
    app = APIFlask(__name__)
    app.config.from_object(conf)

    db.init_app(app)
    migrate.init_app(app, db)
    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)

    csrf.init_app(app)
    security.init_app(app, user_datastore)

    if conf.ENABLE_ADMIN:
        logger.info('enabling admin interface...')
        # set bootswatch theme: http://bootswatch.com/3/
        app.config['FLASK_ADMIN_SWATCH'] = 'journal'
        admin.init_app(app, db)

    logger.info('enabling endpoints...')
    app.register_blueprint(api.bp)

    return app
