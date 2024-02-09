from flask_admin import Admin
from flask_admin.consts import ICON_TYPE_FONT_AWESOME
from webapp import db
# from .routes import CustomView, CustomModelView, CustomFileAdmin
from ..auth.models import User, Role
from ..mainapp.models import Features, Feedback,  Countries, SearcHDestination
from ..users.models import Search

import csv 
admin = Admin()


def create_module(app, **kwargs):
    #admin.init_app(app)
    #admin.add_view(CustomView(name='Custom'))
    #user_model = User
    #models = [user_model, Role, Features, Feedback, SearcHDestination, Search, Countries]
    #for model in models:
    #    admin.add_view(CustomModelView(model, db.session, category='Database Models'))

    #admin.add_view(CustomFileAdmin(app.static_folder,'/static/', name='Static Files'))

    from .routes import admin_blueprint
    app.register_blueprint(admin_blueprint)

