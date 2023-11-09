from flask_security.models import fsqla_v3 as fsqla

from app.storage.db import db


# Leverage flask-security models since a lot of functionality depends on it.
fsqla.FsModels.set_db_info(db)


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = 'role'

    def __repr__(self):
        return self.name


class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = 'user'

    def __repr__(self):
        return self.email
