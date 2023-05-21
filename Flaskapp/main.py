import os
import pickle 

from flask import Flask, redirect, url_for, request, render_template

app= Flask(__name__, instance_relative_config=True, template_folder='templates')


app.config.from_mapping(
        SECRET_KEY='exp',
        DATABASE=os.path.join(app.instance_path, 'pred.sql'),
    )

@app.route('/form')
def index():
    return render_template('form.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return "Enter Details On The Form to Get Predictions."

    if request.method == 'POST':
        details  =  request.post.form
        country  =  details['country']
        age      =  details['age']
        tmale    =  details['tmale']
        tfemale  =  details['tfemale']
        twith    =  details['twith']
        purpose  =  details['purpose']
        activity =  details['activity']
        info     =  details['info']
        tarr     =  details['tarr']
        pint     =  details['pint'] 
        pacc     =  details['pacc']
        pfood    =  details['pfood']
        ptra     =  details['ptra']
        psigh    =  details['psigh']
        pgt      =  details['pgt']
        pins     =  details['pins']
        nmain    =  details['nmain']
        nzanzi   =  details['nzanzi']
        ftrip    =  details['ftrip']  

    
    return render_template('index.html')



if __name__== '__main__':
    app.run(debug=True)