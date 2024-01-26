import os
import csv

from webapp import db, migrate, create_app
from webapp.auth.models import User
from webapp.users.models import Search
from webapp.mainapp.models import Features, Feedback, Countries


env = os.environ.get("LETSGO_ENV", 'prod')
app = create_app('config.%sConfig' % env.capitalize())
        

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Search=Search,
                features=Features, feed=Feedback, country=Countries, migrate=migrate)

def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
