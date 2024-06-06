import logging

import json
import random

import numpy as np

from sqlalchemy import exc

from flask import render_template, url_for, redirect, Blueprint, flash, request, session, jsonify
from flask_login import login_required, current_user

from webapp import db, cache
from webapp.auth.models import User
from .models import Countries, Features, Feedback, SearcHDestination
from .forms import FeaturesForm, feedbackform, search

from ..users.forms import feedback
from ..predict import predict_category, predict_cost, predict_feed_sentiment, staycation
from ..train import train_clf


app_blueprint = Blueprint('app', __name__,
                          static_folder="../static", template_folder="../templates/app", 
                          url_prefix="/letsgo")

@app_blueprint.route("/", methods=['GET', 'POST'])
@cache.cached(timeout=1)
def index():
    users = User.query.all()
    feedback = Feedback.query.all()
    feedback = random.sample(feedback, min(3, len(feedback)))
    
    form = search()
    if request.method == 'POST' and form.validate_on_submit():
        query = form.search.data
        if query:
            session['destination'] = query
            search_query = SearcHDestination(dest=form.search.data)
            db.session.add(search_query)
            db.session.commit()
            return redirect(url_for('app.searchdestination', destination=session.get("destination")))
        flash("Kindly tell us your search destination.")
    return render_template('index.html', users=users,
                            feedback=feedback, form=form, 
                            dest=session.get("destination"), zip=zip)

@app_blueprint.route("/destinations/<destination>")
def searchdestination(destination):
    dest = session.get("destination")
    return render_template("destinations.html", dest=session.get('destination'))

@app_blueprint.route('/form', methods=['GET', 'POST'])
@cache.cached(timeout=2)
def form():    
    form = FeaturesForm(request.form)
    if request.method == 'POST' and form.validate():
        country = form.country.data
        bururi = Countries.query.filter_by(Country=country).first() #Features.bururi.Region
        region = bururi.Region
        sub_region = bururi.Sub_Region
        age = form.age.data
        companion = form.companion.data
        purpose = form.purpose.data
        activity = form.activity.data
        info = form.info.data
        arrangement = form.arrangement.data
        pack_tra_int = form.pack_tra_int.data
        pack_acc = form.pack_acc.data
        main_nights = int(form.main_nights.data)
        zanzi_nights = int(form.zanzi_nights.data)
        duration = main_nights + zanzi_nights
        stay = staycation(duration)
        try:
            submitted = [country, age, companion, purpose, activity, info, arrangement, pack_tra_int,
                     pack_acc, region, sub_region, duration, stay]
            category, probability = predict_category(submitted)
            regress = [country, age, companion, purpose, activity, info, arrangement, pack_tra_int,
                     pack_acc, main_nights, region, sub_region, duration]
            cost = predict_cost(regress)
            if current_user.is_authenticated:
                user_id = current_user.id
            else:
                user_id = None
            features = Features(country=country, region=region, sub_region=sub_region, age_group=age, travel_with=companion, 
                     purpose=purpose, main_activity=activity, info_source=info, tour_arrangement=arrangement, 
                     package_transport_int=pack_tra_int, package_accomodation=pack_acc,
                     night_mainland=main_nights, night_zanzibar=zanzi_nights, duration=duration,
                     staycation=stay, predicted_category=category, probability=probability, total_cost=cost,
                     user_id=user_id)
            db.session.add(features)
            db.session.flush()
            session['feature_id'] = features.id
            session['user'] = features.user_id
            db.session.commit()
            return redirect(url_for('.predict'))
        except exc.IntegrityError as e:
            db.session.rollback() 
            flash("An error occured while generating your predictions", 'warning')
            raise e
    return render_template('app/form.html', form=form)

@app_blueprint.route('/prediction', methods=['POST', 'GET'])
def predict():
    feature_id = session.get('feature_id')
    feature = Features.query.filter_by(id=feature_id).first_or_404()
    if not feature_id or current_user.is_authenticated and ( current_user.id != session.get('user')):
        flash("Kindly provide your travel details first", category="info")
        return redirect(url_for('.form'))
    form = feedback()
    if request.method == 'POST' and form.validate_on_submit():
        feed = form.feed.data
        sentiment, proba = predict_feed_sentiment(feed)
        user_id = current_user.id
        try:
            user_feedback = Feedback(feed=feed, sentiment=sentiment, probability=proba, 
                                 feature_id=feature_id,user_id= user_id)
            db.session.add(user_feedback)
            db.session.commit()
            flash("Thank you for your feedback.", category="info")
            return redirect(url_for('.predict'))
        except exc.IntegrityError as e:
            flash("Your feedback was not sent, our apologies.", category="info")
            logging.error("Error while adding user feedback: {}".format(e))
    return render_template('app/result.html', feature=feature, form=form)

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
