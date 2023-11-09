from flask import url_for, redirect, request, abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from app.models import auth as models


class AuthModelView(ModelView):
    can_delete = False  # disable model deletion
    page_size = 100

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                'superuser' in current_user.roles)

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class RoleView(AuthModelView):
    column_sortable_list = ('name',)


class UserView(AuthModelView):
    column_hide_backrefs = False
    column_list = ('email', 'active', 'last_login_at', 'fs_uniquifier', 'roles')
    column_searchable_list = ('email', 'fs_uniquifier')
    column_filters = ('email', 'fs_uniquifier', 'active', 'roles')
    column_sortable_list = ('last_login_at',)


def init_app(app, db, name='Home', url_prefix='/admin', **kwargs):
    vkwargs = {'name': name, 'endpoint': 'admin', 'url': url_prefix}

    akwargs = {
        'base_template': 'admin/admin_base.html',
        'template_mode': 'bootstrap4',
        'static_url_path': f'/templates/{url_prefix}',
        'index_view': AdminIndexView(**vkwargs),
    }

    admin = Admin(app, **akwargs)
    admin.add_view(RoleView(models.Role, db.session, category='Access'))
    admin.add_view(UserView(models.User, db.session, category='Access'))

    return admin
