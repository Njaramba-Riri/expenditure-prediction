from flask import has_request_context, session, request, current_app
from flask_babel import Babel


def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

babel = Babel(locale_selector=get_locale)

def create_module(app, **kwargs):
    babel.init_app(app)
    from .routes import babel_blueprint
    app.register_blueprint(babel_blueprint)


