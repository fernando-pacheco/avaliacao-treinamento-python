from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields
from sqlalchemy import func
import core.config_app as ca
from core.db import db_instance
from core.models.like import LikeModel
from core.schemas.like import LikeResponseSchema, like_schema, LikeRequestPostSchema, LikeRequestGetSchema
from core.schemas.token import MessageSchema

@doc(description='Like API', tags=['Like'])
class LikeResource(MethodResource, Resource):
    @marshal_with(LikeResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(LikeRequestPostSchema, location='json')
    @doc(description='Create new like')
    def post(self, **kwargs):
        like = LikeModel(**kwargs)
        if like.save():
            return make_response(like_schema.dump(like), 201)
        return make_response({"message": "Fail creating new like"}, 400)

    @use_kwargs({
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location='headers')
    @marshal_with(LikeResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(LikeRequestPostSchema, location='json')
    @use_kwargs(LikeRequestGetSchema, location='query')
    @doc(description='Update saved like')
    @jwt_required()
    def put(self, **kwargs):
        like_id = kwargs["lid"]
        saved_like = LikeModel.find_by_id(like_id)
        if not saved_like:
            return make_response({"message": "Like ID not exists"}, 400)

        saved_like.post_id = kwargs['post_id']
        saved_like.user_id = kwargs['user_id']
        saved_like.save()

        return make_response(like_schema.dump(saved_like), 201)

    @use_kwargs({
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location='headers')
    @marshal_with(LikeResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(LikeRequestGetSchema, location='query')
    @doc(description='Get like by id')
    @jwt_required()
    def get(self, **kwargs):
        like_id = kwargs["lid"]

        like = LikeModel.find_by_id(like_id)
        if like:
            return make_response(like_schema.dump(like), 200)
        return make_response({'message': 'Like not found'}, 404)

    @use_kwargs({
        'Authorization':
        fields.Str(
            required=True,
            description='Bearer [access_token]'
        )
    }, location='headers')
    @marshal_with(MessageSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(LikeRequestGetSchema, location='query')
    @doc(description='Delete like by id')
    @jwt_required()
    def delete(self, **kwargs):
        like_id = kwargs["lid"]

        like = LikeModel.find_by_id(like_id)
        if like:
            like.delete()
            return make_response({'message': 'Like deleted'}, 201)