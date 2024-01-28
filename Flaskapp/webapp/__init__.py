from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
debug_tool = DebugToolbarExtension()
cache = Cache()

def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
    not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('errors/404.html'), 404

def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
    not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('errors/500.html'), 500

def forbidden(e):
    if request.accept_mimetypes.accept_json and \
    not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden', 'message':e})
        response.status_code = 403
        return response
    return render_template('errors/403.html'), 403

def not_allowed(e):
    if request.accept_mimetypes.accept_json and \
    not request.accept_mimetypes.accept_html:
        response = jsonify({"error":"not allowed", "message": e })
        response.status_code = 405
        return response
    return render_template('errors/405.html'), 405

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    from .admin.routes import admin_blueprint
    from .users.routes import user_blueprint
    from .auth.routes import auth_blueprint
    from .mainapp.routes import app_blueprint
    from .api_1_0.routes import api_blueprint

    @app.after_request
    def add_header(response):
        response.cache_control.no_store = True
        return response
    
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    debug_tool.init_app(app)
    cache.init_app(app)

    from .admin import create_module as admin_create_module
    from .babel import create_module as babel_create_module
    from .mainapp import create_module as app_create_module
    from .auth import create_module as auth_create_module
    from .users import create_module as user_create_module
    from .api_1_0 import create_module as api_create_module
    from .api_1_0 import creaate_module as feedback_create_module
    from .dashapp import init_dash

    admin_create_module(app)
    babel_create_module(app)
    app_create_module(app)
    auth_create_module(app)
    user_create_module(app)
    api_create_module(app)
    feedback_create_module(app)

    #app.register_blueprint(admin_blueprint, name="administrator")
    #app.register_blueprint(app_blueprint, name="main application")
    #app.register_blueprint(user_blueprint, name="users")
    #app.register_blueprint(api_blueprint, name="api_app")
    #app.register_blueprint(auth_blueprint, static_url_path='../static/auth/')
    #app.register_blueprint(feedback_create_module, name="feedback_api")
    app.register_error_handler(404, page_not_found) 
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(405, not_allowed)

    app = init_dash(app)
    return app

