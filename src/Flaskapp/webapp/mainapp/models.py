from datetime import datetime, timezone

from webapp import db

class Countries(db.Model):
    """Creates a database model for country names and related details.
    """
    __tablename__ = 'Countries'

    id = db.Column(db.Integer(), primary_key=True)
    Alpha_Code = db.Column(db.String(4), unique=True)
    Country = db.Column(db.String(100))
    Region = db.Column(db.String(20))
    Sub_Region = db.Column(db.String(100))

class Features(db.Model):
    """Creates a database model that stores the features submitted by the user.

    Args:
        db (Sqlalchemy): Base class for all db models.
    """
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
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    date = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    feedback = db.relationship(
        'Feedback', backref='feature', lazy='dynamic'
    )

class Reference_Features(db.Model):
    """Creates a features reference data model for reference features during monitoring.

    Args:
        db (Sqlalchemy): Base class for all db models.
    """
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
    """Creates a database representation where feedback submitted by the user is stored. 

    Args:
        db (Sqlachemy): Base class for all db models.
    """
    __tablename__ ="feedback"

    id = db.Column(db.Integer(), primary_key=True) 
    feed = db.Column(db.String(255), nullable=False)
    sentiment = db.Column(db.String(30), nullable=False)
    probability = db.Column(db.Float())
    feature_id = db.Column(db.Integer(), db.ForeignKey('Features.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    date = db.Column(db.DateTime(), default=datetime.now(timezone.utc))


class SearcHDestination(db.Model):
    """Creates a database representation of the destinations searched by the user.

    Args:
        db (Sqlachemy): Base class for all db models.
    """
    __tablename__ = "destinations"

    id = db.Column(db.Integer(), primary_key=True)
    dest = db.Column(db.String(100), nullable=False)
    found = db.Column(db.String(10), nullable=False)