from flask import Flask, redirect, url_for

app= Flask(__name__, instance_relative_config=True)

@app.route('/predict')
def predict():
    return 'Hello World'

@app.route('/<name>')
def run(name):
    return 'Name is %s!' % name

@app.route('/blog/<int:PostID>')
def new(PostID):
    return 'Your new page is %d'% PostID

@app.route('/new/<float:newno>')
def nasty(newno):
    return 'Your new number %.2f'% newno

if __name__== '__main__':
    app.run(debug=True)