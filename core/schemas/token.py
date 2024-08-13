from marshmallow import Schema, fields


class AccessRefreshTokenUidResponseSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
    uid = fields.Int()


class AccessTokenResponseSchema(Schema):
    access_token = fields.Str()


class AccessRefreshTokenRequestSchema(Schema):
    username = fields.Str(required=True, default='user1', help='Invalid login or password')
    password = fields.Str(required=True, default='pwd1', help='Invalid login or password')


class MessageSchema(Schema):
    message = fields.Str()