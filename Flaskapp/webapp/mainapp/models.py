from webapp import db
import csv
import datetime

class Countries(db.Model):
    __tablename__ = 'Countries'

    id = db.Column(db.Integer(), primary_key=True)
    Alpha_Code = db.Column(db.String(4), unique=True)
    Country = db.Column(db.String(100))
    Region = db.Column(db.String(20))
    Sub_Region = db.Column(db.String(100))

"""
with open("/Users/james/Desktop/expenditure/Datasets/all.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        country = Countries(Country=row["name"], Alpha_Code=row["alpha-3"], Region=row["region"],Sub_Region=row["sub-region"]) 
        
        db.session.add(country)
        db.session.commit() 
"""


class Features(db.Model):
    __tablename__ = "Features"

    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(255))
    age_group = db.Column(db.String(255))
    travel_with = db.Column(db.String(255))
    total_male = db.Column(db.Integer())
    total_female = db.Column(db.Integer())
    purpose  = db.Column(db.String(255))
    main_activity = db.Column(db.String(255))
    info_source = db.Column(db.String(255))
    tour_arrangement = db.Column(db.String(30))
    package_transport_int = db.Column(db.String(10))	
    package_accomodation = db.Column(db.String(10))
    package_food = db.Column(db.String(10))
    package_transport_tz = db.Column(db.String(10))
    package_sightseeing = db.Column(db.String(10))
    package_guided_tour = db.Column(db.String(10))
    package_insurance = db.Column(db.String(10))
    night_mainland = db.Column(db.Integer())
    night_zanzibar = db.Column(db.Integer())
    first_trip_tz = db.Column(db.String(10))
    predicted_category = db.Column(db.String(30))
    probability = db.Column(db.Float())
    total_cost = db.Column(db.Integer())
    cost_probability = db.Column(db.Float())
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    feedback = db.relationship(
        'Feedback', backref='Features', lazy='dynamic'
    )
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

class Reference_Features(db.Model):
    __tablename__ = "Reference_Features"

    id = db.Column(db.String(20), primary_key=True)
    country = db.Column(db.String(255))
    age_group = db.Column(db.String(255))
    travel_with = db.Column(db.String(255))
    total_male = db.Column(db.Integer())
    total_female = db.Column(db.Integer())
    purpose  = db.Column(db.String(255))
    main_activity = db.Column(db.String(255))
    info_source = db.Column(db.String(255))
    tour_arrangement = db.Column(db.String(30))
    package_transport_int = db.Column(db.String(10))	
    package_accomodation = db.Column(db.String(10))
    package_food = db.Column(db.String(10))
    package_transport_tz = db.Column(db.String(10))
    package_sightseeing = db.Column(db.String(10))
    package_guided_tour = db.Column(db.String(10))
    package_insurance = db.Column(db.String(10))
    night_mainland = db.Column(db.Integer())
    night_zanzibar = db.Column(db.Integer())
    first_trip_tz = db.Column(db.String(10))
    actual_category = db.Column(db.String(30))
    predicted_category = db.Column(db.String(30))
    probability = db.Column(db.Float())



class Feedback(db.Model):
    __tablename__ ="feedback"

    id = db.Column(db.Integer(), primary_key=True) 
    feed = db.Column(db.String(255), nullable=False)
    sentiment = db.Column(db.String(30), nullable=False)
    probability = db.Column(db.Float())
    feature_id = db.Column(db.Integer(), db.ForeignKey('Features.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    date = db.Column(db.DateTime(), default=datetime.datetime.now)


class SearcHDestination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer(), primary_key=True)
    dest = db.Column(db.String(100), nullable=False)
    found = db.Column(db.String(10), nullable=False)