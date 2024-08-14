from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import fields
from core.models.comment import CommentModel
from core.schemas.comment import CommentResponseSchema, comment_schema, CommentRequestPostSchema, CommentRequestGetSchema
from core.schemas.token import MessageSchema

@doc(description='Comment API', tags=['Comment'])
class CommentResource(MethodResource, Resource):

    @marshal_with(CommentResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(CommentRequestPostSchema, location='json')
    @doc(description='Create new comment')
    @jwt_required()
    def post(self, **kwargs):
        current_user_id = get_jwt_identity()
        print(current_user_id)
        comment = CommentModel(body=kwargs['body'], author_id=current_user_id, post_id=kwargs['post_id'])
        comment.save()
        return make_response(comment_schema.dump(comment), 201)


    @marshal_with(CommentResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(CommentRequestPostSchema, location='json')
    @use_kwargs(CommentRequestGetSchema, location='query')
    @doc(description='Update saved comment')
    @jwt_required()
    def put(self, **kwargs):
        comment_id = kwargs.get("cid")
        saved_comment = CommentModel.find_by_id(comment_id)
        if not saved_comment:
            return make_response({"message": "Comment não existe"}, 400)

        current_user_id = get_jwt_identity()
        if saved_comment.author_id != current_user_id:
            return make_response({"message": "Não autorizado"}, 403)

        saved_comment.update(**kwargs)
        return make_response(comment_schema.dump(saved_comment), 201)

    @marshal_with(CommentResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(CommentRequestGetSchema, location='query')
    @doc(description='Get comment by id')
    def get(self, **kwargs):
        comment_id = kwargs.get("cid")
        comment = CommentModel.find_by_id(comment_id)
        if comment:
            return make_response(comment_schema.dump(comment), 200)
        return make_response({'message': 'Comment não encontrado'}, 404)


    @marshal_with(MessageSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(CommentRequestGetSchema, location='query')
    @doc(description='Delete comment by id')
    @jwt_required()
    def delete(self, **kwargs):
        comment_id = kwargs.get("cid")
        comment = CommentModel.find_by_id(comment_id)
        if not comment:
            return make_response({'message': 'Comment não encontrado'}, 404)

        current_user_id = get_jwt_identity()
        if comment.author_id != current_user_id:
            return make_response({"message": "Não autorizado"}, 403)

        comment.delete()
        return make_response({'message': 'Comment excluído'}, 201)