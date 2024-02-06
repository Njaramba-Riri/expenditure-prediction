import random
from datetime import datetime

from faker import Faker

from webapp import db
from main import app
from webapp.auth.models import User, Role
from webapp.mainapp.models import Features, Feedback

fake = Faker()

def generate_features(n):
    features = []

    for i in range(n):
        feature = Features()

        choices = ['Yes', 'No']

        feature.country = fake.country()
        random_number = random.choice(range(0, 7))
        feature.age_group = f"{random_number}0-{random_number}9"
        feature.travel_with = random.choice(['ALone', 'Spouse', 'Friends'])
        feature.total_female = random.choice(range(0, 9))
        feature.total_male = random.choice(range(0, 9))
        feature.night_mainland = random.choice(range(0, 30))
        feature.night_zanzibar = random.choice(range(0, 30))
        feature.purpose = random.choice(['Leisure and Holidays', 'Other', 'Volunteering', 'Medical'])
        feature.main_activity = random.choice(['Wildlife Tourism', 'Beach Tourism', 'Cultural Tourism'])
        feature.info_source = random.choice(['Tour agent', 'Friends & Relatives', 'Tanzania mission abroad', 'Radio, Tv', 'Other'])
        feature.tour_arrangement = random.choice(['Package Tour', 'Independent Tour'])
        feature.package_transport_int = random.choice(choices)
        feature.package_transport_tz = random.choice(choices)
        feature.package_accomodation = random.choice(choices)
        feature.package_food = random.choice(choices)
        feature.package_sightseeing = random.choice(choices)
        feature.package_guided_tour = random.choice(choices)
        feature.package_insurance = random.choice(choices)
        feature.first_trip_tz = random.choice(choices)
        feature.predicted_category = random.choice(['High Cost', 'Lower Cost', 'Higher Cost', 'Highest Category', 'Normal Cost'])
        feature.total_cost = random.choice(range(50000, 500000))
        feature.probability = random.choice(range(30, 100))
        feature.cost_probability = random.choice(range(30, 100))
        feature.user_id = random.choice(range(1, 50))

        try:
            db.session.add(feature)
            db.session.commit()
            features.append(feature)
        except:
            db.session.rollback()
    return features

def generate_feedback(n):
    feedback = []

    for i in range(n):
        feed = Feedback()

        now = datetime.now()
        year = now.year
        month = now.month

        feed.feed = fake.sentence()
        feed.sentiment = random.choice(['Positive', 'Negative'])
        feed.probability = random.choice(range(0, 100))
        feed.date = fake.date_time_between_dates(datetime_start=datetime(year, month, 1),
                                                 datetime_end=datetime(year, month+1, 1)
                                                 )
        feed.feature_id = random.choice(range(1, 100))
        feed.user_id = random.choice(range(1, 100))
        
        try:
            db.session.add(feed)
            db.session.commit()
            feedback.append(feed)
        except:
            db.session.rollback()

    return feedback

def generate_users(n, features, feed):
    for i in range(n):
        user = User()

        now = datetime.now()
        month = now.month
        year = now.year

        user.email = fake.email()
        user.username = fake.name()
        password = "testing12"
        user.set_password(password)
        user.about = fake.sentence()
        user.location = fake.address()
        user.confirmed = random.choice([True, False])
        role_name = random.choice(['Administrator', 'User'])
        role = Role.query.filter_by(name=role_name).first()
        if user.role is None:
            user.role = Role(name=role)
        user.date_created = fake.date_this_decade(before_today=True, after_today=False)
        user.last_seen = fake.date_time_between_dates(datetime_start=datetime(year, month, 1),
                                                      datetime_end=datetime(year, month+1, 1))
        
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
        

if __name__ == "__main__":
    with app.app_context():
        generate_feedback(50)
        # generate_users(100, generate_features(50), generate_feedback(40))