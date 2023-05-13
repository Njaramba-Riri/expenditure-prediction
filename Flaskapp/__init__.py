import os

from flask import Flask, redirect, url_for, request, render_template

def create_app(test_config=None):

    app=Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY='exp',
        DATABASE=os.path.join(app.instance_path, 'pred.sql'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/form', methods=['POST', 'GET'])
    def hello():
        return render_template('form.html')


    return app