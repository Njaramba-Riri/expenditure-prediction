import logging

logger = logging.getLogger(__name__)

import functools
import datetime
import requests
import json
from io import StringIO

import numpy as np
import pandas as pd
from pandas import json_normalize

from flask import render_template, redirect, url_for, Blueprint, flash, request, session, abort, jsonify
from flask_login import login_required, current_user
from sqlalchemy import exc

from webapp import db
from webapp.mainapp.models import Features, Feedback
from ..auth.models import User
from .forms import  SearchQuery, editProfile
from .models import Search


user_blueprint = Blueprint("user", __name__,
                           template_folder="templates/users", 
                           static_folder="static/users", url_prefix="/letsgo/user")

@user_blueprint.route("/<username>/profile")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None or current_user.username != username:
        abort(404)
    session['username'] = username
    return render_template("users/myprofile.html", current_time=datetime.datetime.utcnow(),
                           username=session.get('username'), user=user) 

@user_blueprint.route("<username>/edit_profile", methods=['GET', 'POST'])
@login_required
def update(username):
    form = editProfile()
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST' and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.location = form.location.data
        current_user.about = form.about_me.data
        session['username'] = form.username.data
        session['location'] = form.location.data
        session['about']  = form.about_me.data
        db.session.add(user)
        flash("Details Updated.")
        return redirect(url_for('suser.profile', username=current_user.username))
    form.username.data = current_user.username or session.get('username')
    form.location.data = current_user.location or session.get('location')
    form.about_me.data  =current_user.about or session.get('about')
    return render_template('editProfile.html', form=form)

@user_blueprint.route("/<string:username>/activity", methods=['GET', 'POST'])
@login_required
def activity(username):
    if not current_user.is_authenticated:
        flash("Kindly login to access the page")
    user = User.query.filter_by(username=username).first_or_404()
    features = Features.query.filter_by(user_id=user.id).all()
    feedback = Feedback.query.filter_by(user_id=user.id, feature_id=Features.id).all()    
    form = SearchQuery(request.form)
    if request.method == 'POST' and form.validate():
        destination = form.where.data
        adults = form.adults.data
        kids =  form.kids.data
        start = form.checkin.data
        end  =  form.checkout.data
        rooms = form.rooms.data
        try:
            query = Search(destination=destination, total_adults=adults, total_kids=kids,
                        checkin_date=start, checkout_date=end, rooms=rooms, user_id=current_user.id)
            db.session.add(query)
            db.session.commit()
            return redirect(url_for('.get_data'))   
        except exc.IntegrityError as e:
            logger.info("Error while adding destination search: {}".format(e))
            flash("Your search details couldn't be successful.")
            db.session.rollback()
    return render_template("users/activity.html", 
                           features=features, feedback=feedback, 
                           user=user, zip=zip, len=len, form=form)

@user_blueprint.route("/feature/<username>")
@login_required
def get_feature(username):
    user = User.query.filter_by(username=username).first_or_404()
    feature = Features.filter_by(user_id=user.id).all()

    return redirect(url_for('suser.activity'))


@user_blueprint.route("/third-party-api")
@login_required
def get_data():
    query = Search.query.order_by(Search.id.desc()).first_or_404()
    
    if  query:
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"

        querystring = {
            "q":query.destination,
            "locale":"en_US",
            "langid":"1033"
        }

        headers = {
            "X-RapidAPI-Key": "63e04ac616mshf80855038c14955p1a3b69jsn5174b18bfe34",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        respon = requests.get(url, headers=headers, params=querystring)
        info = respon.content
        info = info.decode('utf-8')

        try:
            json_response = json.loads(info)
            datas = respon.json()
            coordinates = json_response['sr'][0]['coordinates']
            lat = coordinates['lat']
            long = coordinates['long']
            regid = json_response['sr'][0]['gaiaId']
        except json.JSONDecodeError as e:
            print(e)
            return jsonify({"Error": "Error trying to decode JSON file."})
        
        query_string = {
            "destination": {
                "coordinates": {
                    "latitude": lat,
                    "longitude": long,
                }
            },
            "checkInDate": {
                "day": query.checkin_date.day,
                "month": query.checkin_date.month,
                "year": query.checkin_date.year
            },
            "checkOutDate": {
                "day": query.checkout_date.day,
                "month": query.checkout_date.month,
                "year": query.checkout_date.year    
            },
            "rooms": [
                {"adults": query.adults,
                "children": query.total_kids
                }
            ]

        }
        
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"
        resp = requests.post(url,  params=query_string, headers=headers)
        data = resp.content
    else:
        return jsonify({"Error": "There was a problem on our side, apologies."}), 500

    try:
        response_json = resp.json()
        #amenities = response_json.get("propertySearch", {}).get("filterMetadata", {}).get("amenities", [])
        amenities = response_json["data"]["propertySearch"]["filterMetadata"]["amenities"]
        neighborhoods = response_json["data"]["propertySearch"]["filterMetadata"]["neighborhoods"]
        pricerange = response_json["data"]["propertySearch"]["filterMetadata"]["priceRange"]

        properties = response_json['data']['propertySearch']['properties'].get('name')
        availability = response_json['data']['propertySearch']['properties']['availability'].get('available')
        roomsleft = response_json['data']['propertySearch']['properties']['availability'].get('minRoomsLeft')
        picture = response_json['data']['propertySearch']['properties']['propertyImage']['image'].get('url')
        coordinates = response_json['data']['propertySearch']['properties']['mapMarker']['latLong'].get({'latitude', 'longitude'})
        pricepriordiscount = response_json['data']['propertySearch']['properties']['price']['options'][0]['strikeOut'].get('formatted')
        priceafterdiscount = response_json['data']['propertySearch']['properties']['price']['options'][0].get('formattedDisplayPrice')
        price_disclaimer = pricepriordiscount = response_json['data']['propertySearch']['properties']['price']['options'][0]['disclaimer'].get('value')
        pricemessage_condition = response_json['data']['propertySearch']['properties']['price']['priceMessages'][0].get('value')
        pricemessage_duration = response_json['data']['propertySearch']['properties']['price']['priceMessages'][1].get('value')


        return render_template("api.html", data=data, 
                               properties=properties, availability=availability, roomsleft=roomsleft,
                               picture=picture, coordinates=coordinates, price=pricepriordiscount,
                               discountedPrice=priceafterdiscount, price_disclaimer=price_disclaimer,
                               price_condition=pricemessage_condition, price_duration=pricemessage_duration,
                               amenities=amenities, neighborhoods=neighborhoods, pricerange=pricerange)
    except json.JSONDecodeError as e:
        print(e)
        #user_blueprint.logger.error(f"JSON decode error: {e}")
        return jsonify({"error": "An error occurred while decoding JSON response"}), 500



@user_blueprint.route("/randomuser")
def get_user():
    response = requests.get("https://randomuser.me/api,")
    data = response.content

    try:
        response_json = json.loads(data)
        print(response_json)
        return data
    except json.JSONDecodeError as e:
        print(e)

        return jsonify({"error": "An error occured while trying to decode JSON response"}), 500


    #return json.loads(data['text'])

@user_blueprint.route("/hotelbeds")
@login_required
def hotelbed():
    url = ""

    query = {"destinantionCode": "",
             "countryCode": "TZ"}
    
    headers = {
        "APIkey" : "eb5f8eba6b4cccee8be32d9cf46e343d",
        "secret": "8bc4ef744b",
        "Xsignature": "8bc4ef744b"
    }