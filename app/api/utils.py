import functools
import json
import uuid

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


def hx_api(f):
    """convert response into js variable in script for htmx to handle"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        resp = f(*args, **kwargs)
        if flask.request.headers.get('Hx-Request'):
            if not isinstance(resp, str):
                resp = json.dumps(resp)
            data_id = str(uuid.uuid4())
            resp = flask.Response(
                '<script id="%s" type="application/json">%s</script>' % (data_id, resp))
            resp.headers['HX-Trigger-After-Swap'] = json.dumps(
                {'apiResponse': {'origin': flask.request.headers.get('Hx-Current-Url'),
                                 'path': flask.request.path, 'dataId': data_id}})
        return resp
    return wrapper
