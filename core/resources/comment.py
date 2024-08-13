from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields
from sqlalchemy import func
import core.config_app as ca
from core.db import db_instance
from core.models.comment import CommentModel
from core.schemas.comment import CommentResponseSchema, comment_schema, CommentRequestPostSchema, CommentRequestGetSchema
from core.schemas.token import MessageSchema

@doc(description='Comment API', tags=['Comment'])
class CommentResource(MethodResource, Resource):
    @marshal_with(CommentResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(CommentRequestPostSchema, location='json')
    @doc(description='Create new comment')
    def post(self, **kwargs):
        comment = CommentModel(**kwargs)
        if comment.save():
            return make_response(comment_schema.dump(comment), 201)
        return make_response({"message": "Fail creating new comment"}, 400)

    @use_kwargs({
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location='headers')
    @marshal_with(CommentResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(CommentRequestPostSchema, location='json')
    @use_kwargs(CommentRequestGetSchema, location='query')
    @doc(description='Update saved comment')
    @jwt_required()
    def put(self, **kwargs):
        comment_id = kwargs["cid"]
        saved_comment = CommentModel.find_by_id(comment_id)
        if not saved_comment:
            return make_response({"message": "Comment ID not exists"}, 400)

        saved_comment.body = kwargs['body']
        saved_comment.post_id = kwargs['post_id']
        saved_comment.author_id = kwargs['author_id']
        saved_comment.save()

        return make_response(comment_schema.dump(saved_comment), 201)

    @use_kwargs({
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location='headers')
    @marshal_with(CommentResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(CommentRequestGetSchema, location='query')
    @doc(description='Get comment by id')
    @jwt_required()
    def get(self, **kwargs):
        comment_id = kwargs["cid"]

        comment = CommentModel.find_by_id(comment_id)
        if comment:
            return make_response(comment_schema.dump(comment), 200)
        return make_response({'message': 'Comment not found'}, 404)

    @use_kwargs({
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location='headers')
    @marshal_with(CommentResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(CommentRequestGetSchema, location='query')
    @doc(description='Delete comment by id')
    @jwt_required()
    def delete(self, **kwargs):
        comment_id = kwargs["cid"]

        comment = CommentModel.find_by_id(comment_id)
        if comment:
            comment.delete()
            return make_response({'message': 'Comment deleted'}, 201)