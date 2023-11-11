from flask import session

from tests.unit import utils


def test_healthcheck(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.text == '¯\\_(ツ)_/¯'


def test_root(client):
    res = client.get('/')
    assert res.status_code == 200
    assert not session


def test_root_login(app_db):
    with utils.authenticated_client(app_db) as client:
        res = client.get('/')
        assert res.status_code == 200
