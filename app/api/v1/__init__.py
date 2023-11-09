from apiflask import APIBlueprint


bp = APIBlueprint('v1', __name__)


from app.api.v1 import auth  # noqa
