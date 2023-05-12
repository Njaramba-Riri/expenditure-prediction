import os
from flask import Flask, redirect, url_for, request, render_template

app= Flask(__name__, instance_relative_config=True, template_folder='templates')


@app.route('/hello')
def index():
    return render_template('hello.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    return render_template('index.html')



if __name__== '__main__':
    app.run(debug=True)