from marshmallow import Schema, fields
from core.schema import ma
from core.models.like import LikeModel

class LikeResponseSchema(ma.Schema):
    id = fields.Int()
    post_id = fields.Int()
    user_id = fields.Int()
    created_at = fields.DateTime()

    class Meta:
        fields = ("id", "post_id", "user_id", "created_at")
        ordered = True

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("like")
        }
    )

class LikeRequestPostSchema(Schema):
    post_id = fields.Int(required=True, default='id', help='Invalid id')

class LikeRequestGetSchema(Schema):
    lid = fields.Int(required=True, default='id', help='Invalid id')

like_schema = LikeResponseSchema()