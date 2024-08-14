from marshmallow import Schema, fields
from core.schema import ma
from core.models.comment import CommentModel

class CommentResponseSchema(ma.Schema):
    id = fields.Int()
    body = fields.Str()
    post_id = fields.Int()
    author_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        fields = ("id", "body", "post_id", "author_id", "created_at", "updated_at")
        ordered = True

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("comment")
        }
    )

class CommentRequestPostSchema(Schema):
    body = fields.Str(required=True, default='body', help='This field cannot be blank')
    post_id = fields.Int(required=True, default='id', help='Invalid id')

class CommentRequestGetSchema(Schema):
    cid = fields.Int(required=True, default='id', help='Invalid id')

comment_schema = CommentResponseSchema()
comment_post_schema = CommentModel(author_id=1, post_id=1, body='some body')