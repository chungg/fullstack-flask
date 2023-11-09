def test_healthcheck(app):
    res = app.test_client().get('/health')
    assert res.status_code == 200
    assert res.text == '¯\\_(ツ)_/¯'
