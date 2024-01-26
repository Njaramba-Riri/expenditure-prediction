import csv

from .models import Countries
from webapp import db

def create_module(app, **kwargs):
    """Creates and registers the main application blueprint. 

    Args:
        app: An instance of flask app.
    """
    from .routes import app_blueprint
    app.register_blueprint(app_blueprint)
      
    with app.app_context():
        countries = Countries.query.all()
        if not countries:
            with open("Datasets/all.csv", 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    country = Countries(Country=row["name"], Alpha_Code=row["alpha-3"], 
                                        Region=row["region"],Sub_Region=row["sub-region"]) 
                    
                    db.session.add(country)
                    db.session.commit()  