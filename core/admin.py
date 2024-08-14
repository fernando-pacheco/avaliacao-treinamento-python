from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from core.models.user import UserModel
from core.models.post import PostModel
from core.models.comment import CommentModel
from core.models.like import LikeModel
from core.models.token import TokenBlocklistModel
from core.db import db_instance
import flask_login as login


class CustomModelView(ModelView):
    def is_accessible(self):
        if login.current_user.is_authenticated:
            return login.current_user.has_role('admin')
        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        # return redirect(url_for('login', next=request.url))
        return False

    column_hide_backrefs = False
    def get_column_names(self, only_columns, excluded_columns):
        return [(c.key, c.name) for c in self.model.__table__.columns]

def config_flask_admin(app):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    admin.add_view(ModelView(UserModel, db_instance.session))
    admin.add_view(ModelView(PostModel, db_instance.session))
    admin.add_view(ModelView(CommentModel, db_instance.session))
    admin.add_view(ModelView(LikeModel, db_instance.session))

    return admin
