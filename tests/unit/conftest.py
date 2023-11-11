import os

import pytest

from app import config
from app.app import create_app
from app.storage.db import db


@pytest.fixture()
def app():
    os.environ.update({
        'SECRET_KEY': 'abc',
        'SECURITY_PASSWORD_SALT': 'abc',
        'SQLALCHEMY_DATABASE_URI': (
            'postgresql://tuser:blah@localhost/demo?options=-c%20search_path=blah'),
    })

    conf = config.get_config().__dict__
    conf.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        # Our test emails/domain isn't necessarily valid
        'SECURITY_EMAIL_VALIDATOR_ARGS': {'check_deliverability': False},
        # Make this plaintext for most tests - reduces unit test time by 50%
        'SECURITY_PASSWORD_HASH': 'plaintext'
    })

    yield create_app(conf)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def app_db(app):
    with app.app_context():
        db.create_all()

        yield app

        # remove session.
        # https://xvrdm.github.io/2017/07/03/testing-flask-sqlalchemy-database-with-pytest/
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
