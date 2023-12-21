from app.api import bp
from app.api import utils


@bp.get('/')
@utils.hx_page('index.html')
def index():
    return {'path': '/'}


@bp.get('/analytics')
@utils.hx_page('analytics.html')
def analytics():
    return {'path': '/analytics'}


@bp.get('/yahoo')
@utils.hx_page('yahoo.html')
def yahoo():
    return {'path': '/yahoo'}
