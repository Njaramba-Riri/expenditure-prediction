import os

from flask import Flask, redirect, url_for, request, render_template

def create_app(test_config=None):

    app=Flask(__name__, instance_relative_config=True, template_folder='templates/app')
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

    # a simple page that says hello
    @app.route('/admin')
    def hello_admin():
        return 'Hello, admin!'

    @app.route('/guest/<guest>')
    def hello_guest(guest):
        return 'Hello %s as guest ' % guest

    @app.route('/user/<name>')
    def hello_user(name):
        if name=='admin':
            return redirect(url_for('hello_admin'))
        else:
            return redirect(url_for('hello_guest', guest=name))


    @app.route('/success/<name>')
    def success(name):
        return 'welcome %s' % name
    
    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method=='POST':
            user= request.form['nm']
            return redirect(url_for('success', name=user))
        else:
            user= request.args.get('nm')
            return redirect(url_for('success', name= user))

    @app.route('/hello/<there>')
    def hello(there):
        return render_template('index.html', name=there)


    @app.route('/hello/<int:score>')
    def hello2(score):
        return render_template('hello.html', marks=score)
    
    
    @app.route('/no')
    def student():
        return render_template('hello.html')

    @app.route('/result',methods = ['POST', 'GET'])
    def result():
         if request.method == 'POST':
            result = request.form
         return render_template("result.html",result = result)
   
    return app