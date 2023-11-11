def create_module(app, **kwargs):
    from .routes import user_blueprint
    app.register_blueprint(user_blueprint, name='suser')
