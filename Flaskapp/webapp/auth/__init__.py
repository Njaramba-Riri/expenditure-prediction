from flask_login import LoginManager, AnonymousUserMixin, login_user, current_user
from flask_bcrypt import Bcrypt
from flask import redirect, url_for, flash, session, abort
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.linkedin import make_linkedin_blueprint, linkedin
from flask_dance.consumer import oauth_authorized
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt_extended import JWTManager
import functools

import os 

from oauthlib.oauth2 import WebApplicationClient
import requests

bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()

login_manager = LoginManager()
login_manager.login_view = "auth.signin" 
login_manager.session_protection = "strong"
login_manager.login_message = "Kindly login to access this page."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(int(userid))

class AppAnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

import functools

def has_role(name):
    def real_decorator(f):
        def wraps(*args, **kwargs):
            if current_user.has_role(name):
                return f(*args, **kwargs)
            else:
                abort(403)
        return functools.update_wrapper(wraps, f)
    return real_decorator


from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

def create_module(app, **kwargs):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)

    linkedin_blueprint = make_linkedin_blueprint(
        client_id=app.config.get("TWITTER_API_KEY"),
        client_secret=app.config.get("TWITTER_API_SECRET")
    )
    app.register_blueprint(linkedin_blueprint, url_prefix="/auth/login")

    facebook_blueprint = make_facebook_blueprint(
        client_id=app.config.get("FACEBOOK_CLIENT_ID"),
        client_secret=app.config.get("FACEBOOK_CLIENT_SECRET")
    )
    app.register_blueprint(facebook_blueprint, url_prefix="/auth/login")

    google_blueprint = make_google_blueprint(
        client_id=app.config.get("GOOGLE_CLIENT_ID"),
        client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
        scope = 'openid https://www.googleapis.com/auth/userinfo.email',
        redirect_url = 'http://127.0.0.1:5000/auth/login/google/authorized'
    )
    app.register_blueprint(google_blueprint, url_prefix="/auth/login")


@oauth_authorized.connect
def logged_in(blueprint, token):
    from ..auth.models import db, User
    if blueprint.name == 'twitter':
        username = session.get('screen_name')
    elif blueprint.name == 'google':
        username = session.get('email')
    elif blueprint.name == 'facebook':
        resp = facebook.get("/me")
        username = resp.json()['name']
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User()
        user.username = username
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash("You have been logged in.", "info")
    redirect(url_for('app.index'))

def authenticate(username, password):
    from .models import User
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    if not user.check_password(password):
        return None
    return user