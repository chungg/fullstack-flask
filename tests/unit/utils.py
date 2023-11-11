from contextlib import contextmanager

from flask import g, session

from app.extensions import security


def init_db():
    roles = ['standard', 'superuser']
    for role in roles:
        security.datastore.find_or_create_role(name=role)

    users = [('basic@blah.ca', 'standard'),
             ('lead@blah.ca', 'superuser')]
    for user, role in users:
        security.datastore.create_user(email=user, password='blah', active=True,
                                       roles=[role])


@contextmanager
def authenticated_client(app, user='basic@blah.ca'):
    init_db()

    client = app.test_client()
    with client:
        res = client.post('/api/login', data={'email': user, 'password': 'blah'},
                          headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert res.headers['location'] == '/'
        assert session
        assert g.identity.user.email == user

        # no idea why but flask-login loses it mind in test_client workflow
        # creates a bunch of contexts and never triggers _load_user which it needs to
        # ultimately set fs_authn_via value
        # alternative is to not actually auth via login url and use FlaskLoginClient
        app.login_manager._load_user()

        yield client
