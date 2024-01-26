from flask import Blueprint, abort
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..mainapp.models import Feedback, db
from ..auth.models import User

from . import feedback, prediction
api_blueprint = Blueprint('api', __name__,
                          url_prefix="/api/v1.0")


feed = {
    'id': fields.Integer(),
    'author': fields.String(attribute=lambda x: x.user.username),
    'feedback': fields.String(),
    'sentiment': fields.String(),
    'probability': fields.String(),
    'feedback_date': fields.DateTime(dt_format='iso8601')
}


