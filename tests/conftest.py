import pytest


SQLALCHEMY_DATABASE_URL = "sqlite://"


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    app.config["WTF_CSRF_ENABLED"] = False
    # Our test emails/domain isn't necessarily valid
    app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}
    # Make this plaintext for most tests - reduces unit test time by 50%
    app.config["SECURITY_PASSWORD_HASH"] = "plaintext"


    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
