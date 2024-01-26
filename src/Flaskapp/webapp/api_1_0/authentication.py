from flask import g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import Serializer
Serializer()

from ..auth.models import User
from .routes import api_blueprint
from .errors import forbidden

auth =  HTTPBasicAuth()

@api_blueprint.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
        not g.current_user.confirmed:
        return forbidden('Unconfirmed account.')

@auth.verify_password
def verify_password(email, password):
    if email == '':
        g.current_user = AnonymousUser()
        return True
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials.')

