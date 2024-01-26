from flask_restful import Api
from .routes import api_blueprint
from .feedback import FeedbackApi

rest = Api()

def creaate_module(app, **kwargs):
       rest.add_resource(
            FeedbackApi,
            '/api/feed',
            '/api/feed/<int:feed_id>')
       rest.init_app(app)


def create_module(app, **kwargs):
    from .routes import api_blueprint
    app.register_blueprint(api_blueprint)