import datetime

from flask import abort
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..mainapp.models import Feedback
from ..auth.models import User

feed = {
    'id': fields.Integer(),
    'author': fields.String(attribute=lambda x: x.user.username),
    'feedback': fields.String(),
    'sentiment': fields.String(),
    'probability': fields.String(),
    'feedback_date': fields.DateTime(dt_format='iso8601')
}

class FeedbackApi(Resource):
    @marshal_with(feed)
    @jwt_required
    def get(self, feed_id=None):
        if feed_id:
            feedback = Feedback.query.get(feed_id)
            if not feedback:
                abort(404)
            return feedback
        else:
            feedbacks = Feedback.query.all()
            return feedbacks
        

