# https://www.doppler.com/blog/environment-variables-in-python
import datetime
import os
from typing import get_type_hints, Union

from dotenv import load_dotenv


class AppConfigError(Exception):
    pass


def _parse_bool(val: Union[str, bool]) -> bool:
    return val if type(val) is bool else val.lower() in ['true', 'yes', '1']


# AppConfig class with required fields, default values, type checking,
# and typecasting for int and bool values
class AppConfig:
    ENV: str = 'test'

    SECRET_KEY: str

    SQLALCHEMY_DATABASE_URI: str

    ENABLE_ADMIN: bool = True

    SECURITY_URL_PREFIX: str = '/api'
    SECURITY_PASSWORD_HASH: str = 'pbkdf2_sha512'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    SECURITY_PASSWORD_SALT: str
    SECURITY_LOGIN_URL: str = '/login'
    SECURITY_LOGOUT_URL: str = '/logout'
    SECURITY_REGISTER_URL: str = '/register'
    SECURITY_LOGIN_USER_TEMPLATE = 'login.html'
    SECURITY_REGISTER_USER_TEMPLATE = 'register.html'

    SECURITY_FLASH_MESSAGES: bool = False
    SECURITY_RECOVERABLE: bool = True
    SECURITY_TRACKABLE: bool = True
    SECURITY_CHANGEABLE: bool = True
    SECURITY_CONFIRMABLE: bool = False
    SECURITY_REGISTERABLE: bool = True
    SECURITY_UNIFIED_SIGNIN: bool = False
    SECURITY_SEND_REGISTER_EMAIL: bool = False

    SECURITY_LOGIN_ERROR_VIEW: str = '/login-error'
    SECURITY_POST_CONFIRM_VIEW: str = "/confirmed"
    SECURITY_CONFIRM_ERROR_VIEW: str = "/confirm-error"
    SECURITY_RESET_VIEW: str = "/reset-password"
    SECURITY_RESET_ERROR_VIEW: str = "/reset-password-error"
    SECURITY_REDIRECT_BEHAVIOR: str = "spa"

    # enforce CSRF protection for session / browser - but allow token-based
    # API calls to go through
    SECURITY_CSRF_PROTECT_MECHANISMS: list = ["session", "basic"]
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS: bool = True

    # Send Cookie with csrf-token. This is the default for Axios and Angular.
    SECURITY_CSRF_COOKIE_NAME: str = "XSRF-TOKEN"
    WTF_CSRF_CHECK_DEFAULT: bool = False
    # TODO: add support for Union/None
    WTF_CSRF_TIME_LIMIT = None

    # have session and remember cookie be samesite (flask/flask_login)
    REMEMBER_COOKIE_SAMESITE: str = "strict"
    SESSION_COOKIE_SAMESITE: str = "strict"

    # This means the first 'fresh-required' endpoint after login will always require
    # re-verification - but after that the grace period will kick in.
    # This isn't likely something a normal app would need/want to do.
    SECURITY_FRESHNESS = datetime.timedelta(minutes=0)
    SECURITY_FRESHNESS_GRACE_PERIOD = datetime.timedelta(minutes=2)

    SECURITY_MSG_INVALID_PASSWORD = ('Invalid user or password.', 'error')
    SECURITY_MSG_USER_DOES_NOT_EXIST = ('Invalid user or password.', 'error')

    """
    Map environment variables to class fields according to these rules:
      - Field won't be parsed unless it has a type annotation
      - Field will be skipped if not in all caps
      - Class field and environment variable name are the same
    """
    def __init__(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, 'NaNone')
            if default_value == 'NaNone' and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            # Cast env var value to expected type and raise AppConfigError on failure
            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise AppConfigError(
                    f'Unable to cast value of "{env[field]}" to '
                    f'type "{var_type}" for "{field}" field'
                )

    def __repr__(self):
        return str(self.__dict__)


def get_config():
    if os.environ.get('ENV') == 'local':
        load_dotenv()

    return AppConfig(os.environ)
