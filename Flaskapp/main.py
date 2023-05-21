import os
import pickle 

from flask import Flask, redirect, url_for, request, render_template
from flask_mysqldb import MySQL

app= Flask(__name__, instance_relative_config=True, template_folder='templates')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 'shadowalker'
app.config['MYSQL_DB']='DB'

mysql=MySQL(app)

app.config.from_mapping(
        SECRET_KEY='exp',
        DATABASE=os.path.join(app.instance_path, 'pred.sql'),
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return "Enter Details On The Form to Get Predictions."

    if request.method == 'POST':
        details  =  request.form
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

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO Users(Country, Age, Total_male, Total_Female, Travel_with, Purpose, Main_activity, Info_Source, Tour_arrangement, Package_Int_Travel,  )")
    results = {}

    return render_template('form.html')



if __name__== '__main__':
    app.run(debug=True)