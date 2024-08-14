from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import fields
from core.models.like import LikeModel
from core.schemas.like import LikeResponseSchema, like_schema, LikeRequestPostSchema, LikeRequestGetSchema
from core.schemas.token import MessageSchema

@doc(description='Like API', tags=['Like'])
class LikeResource(MethodResource, Resource):
    
    @marshal_with(LikeResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(LikeRequestPostSchema, location='json')
    @doc(description='Create new like')
    @jwt_required()
    def post(self, **kwargs):
        current_user_id = get_jwt_identity()
        like = LikeModel(post_id=kwargs['post_id'], author_id=current_user_id)
        like.save()
        return make_response(like_schema.dump(like), 201)


    @marshal_with(LikeResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(LikeRequestPostSchema, location='json')
    @use_kwargs(LikeRequestGetSchema, location='query')
    @doc(description='Update saved like')
    @jwt_required()
    def put(self, **kwargs):
        like_id = kwargs.get("lid")
        saved_like = LikeModel.find_by_id(like_id)
        if not saved_like:
            return make_response({"message": "Like não existe"}, 400)

        current_user_id = get_jwt_identity()
        if saved_like.user_id != current_user_id:
            return make_response({"message": "Não autorizado"}, 403)

        saved_like.update(**kwargs)
        return make_response(like_schema.dump(saved_like), 201)


    @marshal_with(LikeResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(LikeRequestGetSchema, location='query')
    @doc(description='Get like by id')
    def get(self, **kwargs):
        like_id = kwargs.get("lid")
        like = LikeModel.find_by_id(like_id)
        if like:
            return make_response(like_schema.dump(like), 200)
        return make_response({'message': 'Like não encontrado'}, 404)

    @marshal_with(MessageSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(LikeRequestGetSchema, location='query')
    @doc(description='Delete like by id')
    @jwt_required()
    def delete(self, **kwargs):
        like_id = kwargs.get("lid")
        like = LikeModel.find_by_id(like_id)
        if not like:
            return make_response({'message': 'Like não encontrado'}, 404)

        current_user_id = get_jwt_identity()
        if like.user_id != current_user_id:
            return make_response({"message": "Não autorizado"}, 403)

        like.delete()
        return make_response({'message': 'Like excluído'}, 201)
    

@doc(description='Like API', tags=['Like'])
class PostLikeCountResource(MethodResource, Resource):
    @marshal_with(LikeResponseSchema, code=200)
    @doc(description='Get like count for a post by id')
    @jwt_required()
    def get(self, post_id):
        like_count = LikeModel.query.filter_by(post_id=post_id).count()
        return make_response({'post_id': post_id, 'like_count': like_count}, 200)
