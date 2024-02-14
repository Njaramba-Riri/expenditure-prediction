from flask_restful import Api
from .feedback.controllers import FeedbackApi

rest = Api()

def create_module(app, **kwargs):
       rest.add_resource(
            FeedbackApi,
            '/api/feed',
            '/api/feed/<int:feed_id>')
       rest.init_app(app)