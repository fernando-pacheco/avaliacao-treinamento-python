import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy_history import make_versioned
from werkzeug.security import check_password_hash, generate_password_hash

import core.config_app as ca
from core.db import db_instance, db_persist
from core.login_manager import login_manager

make_versioned(user_cls='UserModel')


@login_manager.user_loader
def get_user(user_id):
    return UserModel.query.filter_by(id=user_id).first()


class UserModel(db_instance.Model, UserMixin):
    __versioned__ = {
        'exclude': ['created_at', 'updated_at']
    }
    __tablename__ = 'users'
    __table_args__ = {"schema": ca.DEFAULT_DB_SCHEMA}

    id = db_instance.Column(db_instance.Integer, primary_key=True, index=True)
    username = db_instance.Column(db_instance.String(80), unique=True, nullable=False)
    email = db_instance.Column(db_instance.String(120), unique=True, nullable=False)
    password_hash = db_instance.Column(db_instance.String(200), nullable=False)
    created_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now())
    updated_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return "<UserModel(id={self.id!r}, username={self.username!r}, email={self.email!r})>".format(self=self)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @db_persist
    def save(self):
        db_instance.session.add(self)

    @db_persist
    def delete(self):
        db_instance.session.delete(self)

    @db_persist
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @staticmethod
    def init_data():
        user = UserModel(username="admin", email=f"admin@example.com", password="4210")
        user.save()

sa.orm.configure_mappers()