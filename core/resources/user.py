
from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token
from core.models.user import UserModel
from core.schemas.token import MessageSchema
from core.schemas.user import (UserRequestGetSchema, 
                               UserRequestPostSchema,
                               UserRequestPutSchema,
                               UserResponseSchema, 
                               UserLoginSchema,
                               user_schema)


@doc(description='User Register API', tags=['User'])
class UserRegisterResource(MethodResource, Resource):

    @marshal_with(UserResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(UserRequestPostSchema, location='json')
    @doc(description='Register a new user')
    def post(self, **kwargs):
        if UserModel.find_by_username(kwargs['username']):
            return make_response({"message": "Username ja esta em uso"}, 400)
        
        if UserModel.find_by_email(kwargs['email']):
            return make_response({"message": "Email ja esta em uso"}, 400)

        user = UserModel(username=kwargs['username'], email=kwargs['email'], password=kwargs['password'])
        user.save()
        return make_response({"message": "Cadastro realizado com sucesso", "id": user.id}, 201)


    @marshal_with(UserResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(UserRequestPutSchema, location='json')
    @doc(description='Update saved user')
    @jwt_required()
    def put(self, **kwargs):
        current_user_id = get_jwt_identity()
        saved_user = UserModel.find_by_id(current_user_id)
        if not saved_user:
            return make_response({"message": "User ID nao existe"}, 400)

        if 'password' in kwargs:
            saved_user.set_password(kwargs['password'])
        if 'username' in kwargs:
            saved_user.username = kwargs['username']
        if 'email' in kwargs:
            saved_user.email = kwargs['email']
            
        saved_user.save()

        return make_response(user_schema.dump(saved_user), 201)


    @marshal_with(UserResponseSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(UserRequestGetSchema, location='query')
    @doc(description='Get user by id')
    @jwt_required()
    def get(self, **kwargs):
        user_id = kwargs["uid"]

        user = UserModel.find_by_id(user_id)
        if user:
            return make_response(user_schema.dump(user), 200)
        return make_response({'message': 'User nao encontrado'}, 404)


    @marshal_with(MessageSchema, code=201)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(UserRequestGetSchema, location='query')
    @doc(description='Delete user by id')
    @jwt_required()
    def delete(self, **kwargs):
        current_user_id = get_jwt_identity()

        user = UserModel.find_by_id(current_user_id)
        if user:
            user.delete()
            return make_response({'message': 'User excluido'}, 201)
        return make_response({'message': 'User nao encontrado'}, 404)


@doc(description='User Login API', tags=['User'])
class UserLoginResource(MethodResource, Resource):

    @marshal_with(MessageSchema, code=200)
    @marshal_with(MessageSchema, code=401)
    @use_kwargs(UserLoginSchema, location='json')
    @doc(description='Login a user and return a token')
    def post(self, **kwargs):
        user = UserModel.find_by_email(kwargs['email'])
        if user and user.verify_password(kwargs['password']):
            access_token = create_access_token(identity=user.id)
            return make_response({"access_token": access_token}, 200)
        return make_response({"message": "Email ou senha invalidos"}, 401)