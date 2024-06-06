import functools
from functools import wraps

from sqlalchemy import exc

from flask import redirect, url_for, flash, session, abort
from flask_login import LoginManager, AnonymousUserMixin, login_user, current_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized

login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()

login_manager.login_view = "auth.signin" 
login_manager.session_protection = "strong"
login_manager.login_message = "You need to be logged in for you to access the endpoint."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)

class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        from .models import User
        super(User).__init__()
        self.id = None
        self.username = 'Guest'
        
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


def has_role(name):
    def real_decorator(f):
        def wraps(*args, **kwargs):
            if current_user.has_role(name):
                return f(*args, **kwargs)
            else:
                abort(403)
        return functools.update_wrapper(wraps, f)
    return real_decorator

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
    from .models import Permission
    return permission_required(Permission.ADMINISTER)(f)

def create_module(app, **kwargs):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)

    facebook_blueprint = make_facebook_blueprint(
        client_id=app.config.get("FACEBOOK_CLIENT_ID"),
        client_secret=app.config.get("FACEBOOK_CLIENT_SECRET"),
        redirect_to =  'app.index'
    )
    app.register_blueprint(facebook_blueprint, url_prefix="/auth/login")

    google_blueprint = make_google_blueprint(
        client_id=app.config.get("GOOGLE_CLIENT_ID"),
        client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
        scope = 'openid https://www.googleapis.com/auth/userinfo.email',
        redirect_to = 'app.index'
    )
    app.register_blueprint(google_blueprint, url_prefix="/auth/login")


@oauth_authorized.connect
def logged_in(blueprint, token):
    from ..auth.models import db, User
    if blueprint.name == 'twitter':
        username = session.get('screen_name')
    elif blueprint.name == 'google':
        email = session.get('email')
        username = session.get('name')
    elif blueprint.name == 'facebook':
        resp = facebook.get("/me")
        username = resp.json()['name']
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User()
        user.email = email
        user.username = username
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
    login_user(user)
    flash("Login successful, welcome.", "info")
    return redirect(url_for('app.index'))

def authenticate(username, password):
    from .models import User
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    if not user.check_password(password):
        return "Wrong password."
    return user
