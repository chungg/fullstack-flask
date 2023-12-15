from flask import Flask
from flask_migrate import Migrate
from flask_security import Security
from flask_wtf import CSRFProtect
import requests


class Requests:
    """create request session for reuse across appcontext"""

    def __init__(self, app: Flask = None):
        # alternatively, https://flask.palletsprojects.com/en/2.3.x/appcontext/#storing-data
        self.app = app
        self.session = requests.Session()

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        app.teardown_appcontext(self.teardown)

    def teardown(self, exc: BaseException | None):
        self.session.close()


migrate = Migrate()
security = Security()
csrf = CSRFProtect()
reqs = Requests()
