from apiflask import pagination_builder
from flask import abort
from flask_security import auth_required, roles_accepted, current_user

from app.api.v1 import bp
from app.models import auth as model
from app.schemas import auth as schema
from app.storage.db import db


@bp.get('/users')
@bp.input(schema.UserQuery, location='query')
@bp.output(schema.UsersOut)
@auth_required()
@roles_accepted('superuser')
def list_users(query_data):
    pagination = db.paginate(
        db.select(model.User),
        page=query_data['page'],
        per_page=query_data['per_page']
    )
    users = pagination.items
    return {
        'users': users,
        'pagination': pagination_builder(pagination)
    }


@bp.get('/users/<int:user_id>')
@bp.output(schema.UserOut)
@auth_required()
def get_user(user_id):
    if current_user.id == user_id or any(role.name == 'superuser'
                                         for role in current_user.roles):
        return db.get_or_404(model.User, user_id)
    abort(403)
