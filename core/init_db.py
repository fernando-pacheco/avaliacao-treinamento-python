from sqlalchemy import inspect

from core.db import db_instance
from core.models.user import UserModel
from core.models.post import PostModel
from core.models.like import LikeModel
from core.models.comment import CommentModel


def model_exists(model_class):
    engine = db_instance.get_engine()
    inspector = inspect(engine)
    return inspector.has_table(model_class.__tablename__, model_class.__table_args__["schema"]) \
        or inspector.has_table(model_class.__tablename__)


def init_load_data():
    if model_exists(UserModel):
        UserModel.init_data()
    if model_exists(PostModel):
        pass
    if model_exists(CommentModel):
        pass
    if model_exists(LikeModel):
        pass