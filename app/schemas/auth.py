from apiflask import Schema, PaginationSchema
from apiflask.fields import Integer, String, List, Nested
from apiflask.validators import Range


class UserQuery(Schema):
    page = Integer(load_default=1)
    per_page = Integer(load_default=20, validate=Range(max=100))


class UserOut(Schema):
    fs_uniquifier = String()
    email = String()


class UsersOut(Schema):
    users = List(Nested(UserOut))
    pagination = Nested(PaginationSchema)
