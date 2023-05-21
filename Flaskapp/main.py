import os
import pickle 

from flask import Flask, redirect, url_for, request, render_template
from flask_mysqldb import MySQL

app= Flask(__name__, instance_relative_config=True, template_folder='templates')

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 'shadowalker'
app.config['MYSQL_DB']= 'DB'

mysql=MySQL(app)

app.config.from_mapping(
        SECRET_KEY= 'exp',
        DATABASE=os.path.join(app.instance_path, 'users.sql'),
    )

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return "Enter Details On The Form to Get Predictions."

    if request.method == 'POST':
        details  =  request.form.get
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
        cur.execute("INSERT INTO Users(Country, Age, Total_male, Total_Female, Travel_with, Purpose, Main_activity, Info_Source, Tour_arrangement, Package_Int_Travel, Package_Accomodation, Package_Food, Package_Transport_TZ, Package_SightSeeing, Guided_Tour, Package_Insurance, Nights_MainlandTZ, Nights_Zanzibar, First_Trip) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (country, age, tmale, tfemale, twith, purpose, activity, info, tarr, pint, pacc, pfood, ptra, psigh, pgt, pins, nmain, nzanzi, ftrip))

        mysql.connection.commit()
        cur.close()
        return "Success"
    
    results = {}    
    return render_template('form.html', inplace=True)



if __name__== '__main__':
    app.run(debug=True)