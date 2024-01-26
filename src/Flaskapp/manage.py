import os
from webapp import db, migrate, create_app
from webapp.auth.models import User
from webapp.users.models import Search
from webapp.mainapp.models import Features, Feedback, Countries
import csv

env = os.environ.get("LETSGO_ENV", 'prod')
app = create_app('config.%sConfig' % env.capitalize())

"""
with app.app_context():
    with open("/Users/james/Desktop/expenditure/Datasets/all.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            country = Countries(Country=row["name"], Alpha_Code=row["alpha-3"], Region=row["region"],Sub_Region=row["sub-region"]) 
            
            db.session.add(country)
            db.session.commit() 
"""         

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Search=Search,
                features=Features, feed=Feedback, migrate=migrate)

def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
