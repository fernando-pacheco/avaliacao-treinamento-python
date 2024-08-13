from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields
from sqlalchemy import func
import core.config_app as ca
from core.db import db_instance
from core.models.post import PostModel
from core.schemas.post import PostResponseSchema, post_schema, PostRequestPostSchema, PostRequestGetSchema
from core.schemas.token import MessageSchema
from sqlalchemy.exc import IntegrityError

@doc(description='Post API', tags=['Post'])
class PostResource(MethodResource, Resource):
    @marshal_with(PostResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(PostRequestPostSchema, location='json')
    @doc(description='Create new post')
    def post(self, **kwargs):
        post = PostModel(**kwargs)
        post.save()
        return make_response(post_schema.dump(post), 201)

    @use_kwargs({
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location='headers')
    @marshal_with(PostResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(PostRequestPostSchema, location='json')
    @use_kwargs(PostRequestGetSchema, location='query')
    @doc(description='Update saved post')
    @jwt_required()
    def put(self, **kwargs):
        post_id = kwargs["pid"]
        post = PostModel.find_by_id(post_id)

        if not post:
            return make_response({"message": "Post not exists"}, 400)       

        post.update(**kwargs)
        return make_response(post_schema.dump(post), 201)

    @use_kwargs({
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location='headers')
    @marshal_with(PostResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(PostRequestGetSchema, location='query')
    @doc(description='Get post by id')
    @jwt_required()
    def get(self, **kwargs):
        post_id = kwargs["pid"]

        post = PostModel.find_by_id(post_id)
        if post:
            return make_response(post_schema.dump(post), 200)
        return make_response({'message': 'Post not exists'}, 404)

    @use_kwargs({
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location='headers')
    @marshal_with(PostResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(PostRequestGetSchema, location='query')
    @doc(description='Delete post by id')
    @jwt_required()
    def delete(self, **kwargs):
        post_id = kwargs["pid"]

        post = PostModel.find_by_id(post_id)
        if post:
            post.delete()
            return make_response({'message': 'Post deleted'}, 201)
        return make_response({'message': 'Post not found'}, 404)