def create_module(app, **kwargs):
    from .routes import app_blueprint
    app.register_blueprint(app_blueprint)
    