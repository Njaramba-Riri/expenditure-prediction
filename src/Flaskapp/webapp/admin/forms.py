from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField ,widgets, TelField, SearchField
from wtforms import ValidationError, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Email, Regexp
from ..auth.models import User, Role

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
    email = StringField("Enter new email", validators=[DataRequired(), Email()])
    username = StringField("Enter new username", validators=[DataRequired(), Length(1, 64), 
                                                         Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    role = SelectField("Assign role", coerce=int)
    mobile = TelField("Enter mobile number", validators=[Optional()])
    location = StringField("Where are you from?", validators=[Optional(), Length(1, 100)])
    about = StringField("User bio if you like.", validators=[Optional(), Length(1, 255)])
    company = StringField("Enter your tour agency name.", validators=[Optional(), Length(5, 100)])
    c_email = StringField("Enter company email", validators=[DataRequired(), Email()])
    c_mobile = TelField("Enter company telephone number.", validators=[DataRequired()])
    c_address = StringField("Your tour agency location address.", validators=[DataRequired(), Length(10, 64)])
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

    def validate_c_email(self, field):
        if self.data != self.user.company_email and User.query.filter_by(company_email=field.data).first():
            raise ValidationError("The given company email already exists.")    

    def validate_mobile(self, field):
        if len(field.data ) < 10:
            raise ValidationError("Enter a valid tel number.")


    