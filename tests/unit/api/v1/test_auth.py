from tests.unit import utils


def test_list_users(app_db):
    with utils.authenticated_client(app_db, user='lead@blah.ca') as client:
        res = client.get('/api/v1/users', content_type='application/json')
        assert res.status_code == 200
        res = res.json
        assert len(res['users']) == 2
        assert res['pagination']['pages'] == 1
        assert res['pagination']['total'] == 2


def test_list_users_wrong_role(app_db):
    client = app_db.test_client()
    res = client.get('/api/v1/users', content_type='application/json')
    assert res.status_code == 401

    with utils.authenticated_client(app_db, user='basic@blah.ca') as client:
        res = client.get('/api/v1/users', content_type='application/json')
        assert res.status_code == 403


def test_get_user(app_db):
    with utils.authenticated_client(app_db, user='basic@blah.ca') as client:
        res = client.get('/api/v1/users/1', content_type='application/json')
        assert res.status_code == 200
        assert res.json['email'] == 'basic@blah.ca'
        assert res.json.keys() == {'email', 'fs_uniquifier'}

        res = client.get('/api/v1/users/2', content_type='application/json')
        assert res.status_code == 403


def test_get_user_super(app_db):
    with utils.authenticated_client(app_db, user='lead@blah.ca') as client:
        res = client.get('/api/v1/users/1', content_type='application/json')
        assert res.status_code == 200
        assert res.json['email'] == 'basic@blah.ca'
        assert res.json.keys() == {'email', 'fs_uniquifier'}

        res = client.get('/api/v1/users/2', content_type='application/json')
        assert res.status_code == 200
        assert res.json['email'] == 'lead@blah.ca'
