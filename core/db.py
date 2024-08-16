from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import redis

import core.config_app as ca

db_instance = SQLAlchemy()


def config_sql_alchemy(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = ca.DEFAULT_DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = ca.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_ECHO'] = ca.SQLALCHEMY_ECHO
    db_instance.app = app
    db_instance.init_app(app)


redis_instance = redis.Redis(host=ca.REDIS_HOST, port=ca.REDIS_PORT, password=ca.REDIS_PWD, decode_responses=True)

def db_persist(func):
    def persist(*args, **kwargs):
        func(*args, **kwargs)
        try:
            db_instance.session.commit()
            return True
        except SQLAlchemyError as e:
            print(e)
            db_instance.session.rollback()
            return False
    return persist