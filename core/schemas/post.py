from marshmallow import Schema, fields
from core.schema import ma
from core.models.post import PostModel
from core.schemas.comment import CommentResponseSchema

class PostResponseSchema(ma.Schema):
    id = fields.Int()
    title = fields.Str()
    body = fields.Str()
    author_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        fields = ("id", "title", "body", "author_id", "created_at", "updated_at")
        ordered = True

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("post")
        }
    )

class PostRequestPostSchema(Schema):
    title = fields.Str(required=True, default='title', help='This field cannot be blank')
    body = fields.Str(required=True, default='body', help='This field cannot be blank')

class PostRequestGetSchema(Schema):
    pid = fields.Int(required=True, default='id', help='Invalid id')

class PostDetailResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    body = fields.Str()
    author_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    comments = fields.List(fields.Nested(CommentResponseSchema))
    likes = fields.Int()

    class Meta:
        fields = ("id", "title", "body", "author_id", "created_at", "updated_at", "comments", "likes")
        ordered = True


post_detail_schema = PostDetailResponseSchema()
post_schema = PostResponseSchema()
post_post_schema = PostModel(title='some title', body='some body', author_id=1)