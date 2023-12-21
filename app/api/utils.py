import functools
import json

import flask


def hx_page(template):
    """set response header to trigger event to initialise frontend assets (if needed)"""
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            ctx = f(*args, **kwargs)
            resp = flask.Response(flask.render_template(template_name))
            resp.headers['HX-Trigger-After-Settle'] = json.dumps({'initPage': ctx})
            return resp
        return decorated_function
    return decorator
