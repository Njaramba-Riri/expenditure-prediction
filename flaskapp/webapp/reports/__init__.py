def create_module(app, **kwargs):
    from .routes import reports_blueprint
    
    app.register_blueprint(reports_blueprint)
