from flask_wtf import FlaskForm
from .models import Countries
from webapp import db
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, ValidationError
import csv


class FeaturesForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country.choices = [('', '----')] + [(c.Country, c.Country) for c in Countries.query.all()]

    country = SelectField("Country: ", validators=[DataRequired()])
    age = SelectField("Age Group: ", choices=[('', '----'), ("1-17", "Below 18"), ("18-24", "18-24"), 
                                            ("25-44", "25-44"), ("45-64", "45-64"), ("65-100", "Above 64")],
                                            validators=[DataRequired(), Length(min=3)])
    companion = SelectField("Travel Companion: ", choices=[('', '----'), ("Alone", "Alone"), ("With Spouse", "Spouse"), 
                                                         ("With Children", "Children"), ("With Spouse and Children", "Spouse and Children"),
                                                         ("With Other Friends/Relatives", "Friends")], validators=[DataRequired()])
    main_nights = IntegerField("Nights In Mainland TZ: ", validators=[InputRequired(message="Kindly enter a positive value."),
                                                                             NumberRange(min=0, max=365)])
    zanzi_nights = IntegerField("Nights In Zanzibar: ", validators=[InputRequired(), NumberRange(min=0, max=365)]) 
    purpose  = SelectField("Travel Purpose: ", choices=[('', '----'), ("Leisure and Holidays", "Leisure/Holidays" ), 
                                                      ("Visiting Friends and Relatives", "Visiting Friends/Relatives"),
                                                      ("Business", "Business"), ( "Meetings and Confrence", "Meeting/Conference"), 
                                                      ("Scientific and Academic", "Scientific and Academic"), 
                                                      ("Volunteering", "Volunteering"), ("Medical", "Medical"), 
                                                      ("Other", "Other")], validators=[DataRequired()])
    activity = SelectField("Main Activity: ", choices=[('', '----'), ("Wildlife Tourism", "Wildlife Tourism"), 
                                                       ("Beach Tourism", "Beach Tourism"), ("Hunting Tourism", "Hunting Tourism"), 
                                                       ("Cultural Tourism", "Cultural Tourism"), ("Mountain Climbing", "Mountain Climbing"), 
                                                       ("Bird Tourism", "Bird Tourism"), ("Conference Tourism", "Conference Tourism"), 
                                                       ("Diving and Sport Fishing", "Diving and Sport Fishing")], validators=[DataRequired()])
    info = SelectField("Source of Information: ", choices=[('', '----'), ("Others", "Others"), 
                                                           ("Travel agent, tour operator", "Tour Agent/Operator"),
                                                           ("Radio, TV, Web", "Radio/TV/Social Media"),
                                                           ("Friends, relatives", "Friends/Relatives"), 
                                                           ("Inflight magazines", "Inflight Magazines"), 
                                                           ('Trade fair', "Trade Fair"),
                                                           ('Newspaper, magazines, brochures', "Newspaper/Magazines/Brochures"),
                                                           ('Tanzania Mission Abroad', "Tanzania Mission Abroad")], validators=[DataRequired()])
    arrangement = SelectField("Your Tour Arrangement: ", choices=[('', '----'), ("Independent", "Independent Tour"),
                                                              ("Package Tour", "Package Tour")], validators=[DataRequired()])
    pack_tra_int = SelectField("Transport International?: ", choices=[('', '----'), ("Yes", "Yes"), 
                                                                        ("No", "No")], validators=[DataRequired()])
    pack_acc = SelectField("Package Accomodation?: ", choices=[('', '----'), ("Yes", "Yes"),
                                                      ("No", "No")], validators=[DataRequired()])
    submit = SubmitField("Generate Predictions")   
    
    
    def validate_fields(self, field):
        if field.data is None:
            raise ValidationError(f"Kindly ensure {field.label.text} is selected.")

class search(FlaskForm):
    search = StringField("Search Destination", validators=[DataRequired(), Length(max=64)])

class feedbackform(FlaskForm):
    feed = TextAreaField("Kindly give us your feedback below.", 
                         validators=[DataRequired(), Length(max=200)])
