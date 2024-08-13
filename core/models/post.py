from sqlalchemy.sql import func
from sqlalchemy_history import make_versioned
from sqlalchemy.dialects.postgresql import TEXT
import core.config_app as ca
from core.db import db_instance, db_persist

make_versioned(user_cls='PostModel')

class PostModel(db_instance.Model):
    __versioned__ = {
        'exclude': ['created_at', 'updated_at']
    }
    __tablename__ = 'posts'
    __table_args__ = {"schema": ca.DEFAULT_DB_SCHEMA}

    id = db_instance.Column(db_instance.Integer, primary_key=True, index=True)
    title = db_instance.Column(db_instance.String(200))
    body = db_instance.Column(TEXT(), default='')
    author_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey(f'{ca.DEFAULT_DB_SCHEMA}.users.id'))
    created_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now())
    updated_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __init__(self, title, body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id
        
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
    def find_by_id(cls, post_id):
        return cls.query.filter_by(id=post_id).first()
    
    @classmethod
    def find_by_author_id(cls, author_id):
        return cls.query.filter_by(author_id=author_id).all()