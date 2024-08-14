from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import fields
from core.models.post import PostModel
from core.models.comment import CommentModel
from core.models.like import LikeModel
from core.schemas.post import PostResponseSchema, post_schema, PostRequestPostSchema, PostRequestGetSchema
from core.schemas.token import MessageSchema
from core.schemas.comment import CommentResponseSchema


@doc(description='Post API', tags=['Post'])
class PostResource(MethodResource, Resource):

    @marshal_with(PostResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(PostRequestPostSchema, location='json')
    @doc(description='Create new post')
    @jwt_required()
    def post(self, **kwargs):
        current_user_id = get_jwt_identity()
        post = PostModel(title=kwargs['title'], body=kwargs['body'], author_id=current_user_id)
        post.save()
        return make_response(post_schema.dump(post), 201)

    @marshal_with(PostResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(PostRequestPostSchema, location='json')
    @use_kwargs(PostRequestGetSchema, location='query')
    @doc(description='Update saved post')
    @jwt_required()
    def put(self, **kwargs):
        post_id = kwargs.get("pid")
        post = PostModel.find_by_id(post_id)

        if not post:
            return make_response({"message": "Post não encontrado"}, 400)
        
        current_user_id = get_jwt_identity()
        if post.author_id != current_user_id:
            return make_response({"message": "Não autorizado"}, 403)
        
        post.update(**kwargs)
        return make_response(post_schema.dump(post), 201)


    @marshal_with(PostResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(PostRequestGetSchema, location='query')
    @doc(description='Get post by id')
    def get(self, **kwargs):
        post_id = kwargs.get("pid")
        post = PostModel.query.get(post_id)
        if not post:
            return make_response({"message": "Post não encontrado"}, 404)
        
        comments = CommentModel.query.filter_by(post_id=post_id).all()
        like_count = LikeModel.query.filter_by(post_id=post_id).count()

        post_data = post_schema.dump(post)
        post_data['comments'] = CommentResponseSchema(many=True).dump(comments)
        post_data['likes'] = like_count

        return make_response(post_data, 200)

    @marshal_with(PostResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(PostRequestGetSchema, location='query')
    @doc(description='Delete post by id')
    @jwt_required()
    def delete(self, **kwargs):
        post_id = kwargs.get("pid")

        post = PostModel.find_by_id(post_id)
        if not post:
            return make_response({'message': 'Post não encontrado'}, 404)
        
        current_user_id = get_jwt_identity()
        if post.author_id != current_user_id:
            return make_response({"message": "Não autorizado"}, 403)
        
        post.delete()
        return make_response({'message': 'Post excluído'}, 201)

@doc(description='Post API', tags=['Post'])
class PostGetAllResource(MethodResource, Resource):
    @marshal_with(PostResponseSchema, code=200)
    @doc(description='Get all posts')
    def get(self):
        posts = PostModel.query.all()
        return make_response(post_schema.dump(posts, many=True), 200)