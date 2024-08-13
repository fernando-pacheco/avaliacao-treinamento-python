from marshmallow import Schema, fields
from core.schema import ma


class UserResponseSchema(ma.Schema):
    id = fields.Int()
    username = fields.Str()

    class Meta:
        fields = ("id", "username")
        ordered = True

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("user")
        }
    )


class UserRequestPostSchema(Schema):
    username = fields.Str(required=True, default='user1', help='This field cannot be blank')
    password = fields.Str(required=True, default='pwd1', help='This field cannot be blank')


class UserRequestGetSchema(Schema):
    uid = fields.Int(required=True, default='id', help='Invalid id')


user_schema = UserResponseSchema()
user_post_schema = UserRequestPostSchema()