from flask import render_template, url_for, redirect, Blueprint, flash, request, session, jsonify
from flask_login import login_required, current_user

from .models import Features, Feedback, SearcHDestination
from webapp.auth.models import User
from .forms import FeaturesForm, feedbackform, search
from webapp import db
from .. import cache
import random

import requests

import numpy as np
from ..predict import predict_details, predict_feed_sentiment

app_blueprint = Blueprint('app', __name__,
                          static_folder="../static",
                          template_folder="../templates/app", 
                          url_prefix="/letsgo")

@app_blueprint.route("/", methods=['GET', 'POST'])
@cache.cached(timeout=60)
def index():
    users = User.query..all()
    feedback = Feedback.query.all()
    feedback = random.sample(feedback, min(3, len(feedback)))
    
    form = search()
    if request.method == 'POST' and form.validate_on_submit():
        query = form.search.data
        if query:
            session['destination'] = query
            searchq = searcHDestination(dest=form.search.data)
            db.session.add(searchq)
            return redirect(url_for('app.searchdestination', destination=session.get("destination")))
    return render_template('index.html', users=users,
                            feedback=feedback, form=form, zip=zip)

@app_blueprint.route("/destinations/<destination>")
def searchdestination(destination):
    dest = session.get("destination")
    return render_template("app/destinations.html", dest=session.get('destination'))

@app_blueprint.route('/form', methods=['GET', 'POST'])
@cache.cached(timeout=60)
def form():    
    form = FeaturesForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        country        =  form.country.data
        age            =  form.age.data
        companion      =  form.companion.data
        male           =  int(form.male.data)
        female         =  int(form.female.data)
        purpose        =  form.purpose.data
        activity       =  form.activity.data
        info           =  form.info.data
        arrangement    =  form.arrangement.data
        pack_tra_int   =  form.pack_tra_int.data
        pack_tra_tz    =  form.pack_tra_tz.data
        pack_acc       =  form.pack_acc.data
        pack_food      =  form.pack_food.data
        pack_sigh      =  form.pack_sight.data
        pack_guide     =  form.pack_guide.data
        pack_insurance =  form.pack_insurance.data
        main_nights    =  int(form.main_nights.data)
        zanzi_nights   =  form.zanzi_nights.data
        freq           =  form.freq.data

        features = Features(country=country, age_group=age, travel_with=companion, total_male=male, total_female=female, purpose=purpose, main_activity=activity, info_source=info, tour_arrangement=arrangement, package_transport_int=pack_tra_int, package_transport_tz=pack_tra_tz , package_accomodation=pack_acc, package_food=pack_food,package_sightseeing=pack_sigh, package_guided_tour=pack_guide, package_insurance=pack_insurance, night_mainland=main_nights, night_zanzibar=zanzi_nights, first_trip_tz=freq)

        db.session.add(features)

        return redirect(url_for('app.predict'))
    
    return render_template('app/form.html', form=form)

@app_blueprint.route('/prediction', methods=['GET', 'POST'])
def predict():

    details = Features.query.order_by(Features.id.desc()).first()

    # Extract the input features (X) from the last transaction
    X = np.array((details.country, details.age_group, details.travel_with, details.total_male, details.total_female,
         details.purpose, details.main_activity, details.info_source, details.tour_arrangement,
         details.package_transport_int, details.package_transport_tz, details.package_accomodation,
         details.package_food, details.package_sightseeing, details.package_guided_tour,
         details.package_insurance, details.night_mainland, details.night_zanzibar,
         details.first_trip_tz))
    
    pred, probability = predict_details(X)
    details.predicted_category = pred
    details.probability = probability
    if current_user.is_authenticated:
        details.user_id = current_user.id
    db.session.commit()

    return render_template('app/result.html', features=details, predicted_result=pred, probability=f"{probability}")


@app_blueprint.route('/thanks', methods=['GET', 'POST'])
@login_required
def thanks():
    if request.method == 'POST':
        feed = request.form['feedback_button']
        if feed == 'Disatisfied':
                return redirect(url_for('app.sema'))
        flash("Thank you, we're very happy to hear that. 🤗🎆🎇", category='info')
    return render_template('app/thanks.html')


@app_blueprint.route('/feedback', methods=['GET', 'POST'])
@login_required
def sema():
    form = feedbackform(request.form)
    if request.method == 'POST':
        feed = form.feed.data
        senti, proba = predict_feed_sentiment(feed)
        details = Features.query.order_by(Features.id.desc()).first()
        id = details.id
        uhoro = Feedback(feed=feed, sentiment=senti, probability=proba, feature_id=id, user_id=current_user.id)

        db.session.add(uhoro)
        db.session.commit() 

        flash('Feedback received, thank you for your time.')
        return redirect(url_for('suser.activity', username=current_user.username))
 
    return render_template('app/feedback.html', form=form)


