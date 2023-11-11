from apiflask import APIBlueprint

from app.api.v1 import bp as bp_v1


bp = APIBlueprint('api', __name__)


from app.api import root  # noqa


bp.register_blueprint(bp_v1, url_prefix='/api/v1')
