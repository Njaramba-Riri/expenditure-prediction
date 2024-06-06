from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField ,widgets, TelField, SearchField
from wtforms import ValidationError, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Email, Regexp
from ..auth.models import User, Role
from .models import Admin

class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class UsersForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user.choices = [(None, '')] + [ u.email for u in User.query.all()]

    user = SearchField("Search user by email", validators=[Optional(), Email(), Length(1, 64)])
    user_id = IntegerField("Search user by id", validators=[Optional()]) 
    search = SubmitField("Search")

class editProfile(FlaskForm):
    email = StringField("Assign user new email", validators=[Optional(), Email()])
    name = StringField("User full name", validators=[Optional(), Length(max=100)])
    username = StringField("Assign user new username", validators=[Optional(), Length(min=4, max=64), 
                                                         Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    role = SelectField("Assign new role", coerce=int)
    mobile = TelField("Enter user mobile number", validators=[Optional()])
    location = StringField("User location?", validators=[Optional(), Length(1, 100)])
    about = StringField("Add user bio.", validators=[Optional(), Length(1, 255)])
    confirmed = BooleanField("Confirmed", validators=[Optional()])

    def __init__(self, user, *args, **kwargs):
        super(editProfile, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if self.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError("The given email already exists.")
        
    def validate_username(self, field):
        if self.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError("The given username already exists.")

    def validate_mobile(self, field):
        if len(field.data ) < 10:
            raise ValidationError("Enter a valid tel number.")



class editAdmin(FlaskForm):
    name = StringField("Admin full name.", validators=[DataRequired(), Length(min=10, max=50)])
    email = StringField("Email address", validators=[Optional(), Email()])
    mobile = TelField("Mobile number", validators=[Optional()])
    agency = StringField("Tour Company name", validators=[DataRequired(), Length(max=100)])
    agency_email = StringField("Company email address", validators=[DataRequired(), Email()])
    agency_mobile = TelField("Company office line/mobile", validators=[DataRequired()])
    agency_address = StringField("Company physical address", validators=[DataRequired(), Length(max=200)])

    def validate_email(self, field):
        if self.data != self.email and Admin.query.filter_by(email=field.data).first():
            if current_user.email != self.email:
                raise ValidationError("Given email address already exists")

        if self.data != self.email and current_user.email == field.data:
            raise ValidationError("Your current email can't be your new email.")
    
    def validate_username(self, field):
        if self.data != self.username and User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already exists")
        
    def validate_mobile(self, field):
        if len(field.data) < 9 or len(field.data) > 20:
            raise ValidationError("Enter a valid mobile number.")
        
    def validate_agency_mobile(self, field):
        if len(field.data) < 9 or len(field.data) > 20:
            raise ValidationError("Enter a valid company office number.")