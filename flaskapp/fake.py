import random
from datetime import datetime

from faker import Faker

from webapp import db
from main import app
from webapp.auth.models import User, Role
from webapp.mainapp.models import Features, Feedback, Countries
from webapp.predict import staycation

fake = Faker()

def generate_features(n):
    features = []

    for i in range(n):
        feature = Features()

        choices = ['Yes', 'No']

        feature.country = fake.country()
        cout = Countries.query.filter_by(Country=feature.country).first()
        feature.region = cout.Region
        feature.sub_region = cout.Sub_Region
        feature.age_group = random.choice(['1-17', '18-24', '25-44', '45-64','65-100'])
        feature.travel_with = random.choice(['Alone', 'Spouse', 'Friends'])
        feature.night_mainland = random.choice(range(0, 30))
        feature.night_zanzibar = random.choice(range(0, 30))
        feature.purpose = random.choice(['Leisure and Holidays', 'Other', 'Volunteering', 'Medical'])
        feature.main_activity = random.choice(['Wildlife Tourism', 'Beach Tourism', 'Cultural Tourism'])
        feature.info_source = random.choice(['Tour agent', 'Friends & Relatives', 'Tanzania mission abroad', 'Radio, Tv', 'Other'])
        feature.tour_arrangement = random.choice(['Package Tour', 'Independent Tour'])
        feature.package_transport_int = random.choice(choices)
        feature.package_transport_tz = random.choice(choices)
        feature.package_accomodation = random.choice(choices)
        feature.duration = feature.night_mainland + feature.night_zanzibar
        feature.staycation = staycation(feature.duration)
        feature.predicted_category = random.choice(['High Cost', 'Lower Cost', 'Higher Cost', 
                                                    'Highest Cost', 'Normal Cost'])
        feature.total_cost = random.choice(range(100000, 500000))
        feature.probability = random.choice(range(30, 100))
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
        feed.probability = random.choice(range(50, 100))
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
        user.full_name = fake.name()
        user.username = (user.full_name).split()[0]
        password = "testing12"
        user.set_password(password)
        user.about = fake.sentence()
        user.location = f"{fake.city()}, {fake.country()}"
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
        # generate_feedback(50)
        generate_users(20, generate_features(1000), generate_feedback(30))
