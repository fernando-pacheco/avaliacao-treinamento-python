from flask_restful import Api

from core.resources.health_checker import HealthCheckerResource
from core.resources.token import TokenRefresherResource, TokenResource
from core.resources.user import UserRegisterResource
from core.resources.post import PostResource
from core.resources.like import LikeResource
from core.resources.comment import CommentResource


def config_app_routes(app, docs):
    api = Api(app)
    __setting_route_doc(UserRegisterResource, '/user', api, docs)
    __setting_route_doc(TokenResource, '/token', api, docs)
    __setting_route_doc(TokenRefresherResource, '/token/refresh', api, docs)
    __setting_route_doc(LikeResource, '/like', api, docs)
    __setting_route_doc(PostResource, '/post', api, docs)
    __setting_route_doc(CommentResource, '/comment', api, docs)
    return api


def __setting_route_doc(resource, route, api, docs):
    api.add_resource(resource, route)
    docs.register(resource)