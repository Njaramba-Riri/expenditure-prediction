from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, IntegerField, ValidationError, FileField
from wtforms.validators import DataRequired, Length, EqualTo, URL, Optional, NumberRange, Email, Regexp
from ..auth.models import User
from flask_login import current_user

class user_register(FlaskForm):
    email = StringField("Enter your Email ", validators=[DataRequired(), Length(1, 64) , Email()])
    username = StringField("Username: ", validators=[DataRequired(), Length(1, 64),
                                                      Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField("Confirm Password: ", validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already exists, login instead.")

    def validate_usenamer(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")



class user_signin(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in.")
    
    def validate(self, extra_validators=None):
        check_validate =  super(user_signin, self).validate(extra_validators)
        if not check_validate:
            return False
        #User exists?
        user =  User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append("Invalid Credentials.")
            return False
        #check password match
        if not user.check_password(self.password.data):
            self.username.errors.append("Invalid Credentials.")
            return False
        return True
    
class changePass(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), EqualTo('confirm', 
                                                                                     message='Passwords must match.')])
    confirm= PasswordField('Confirm new password', validators=[DataRequired()])

class forgot(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])


class forgotPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    
class editProfile(FlaskForm):
    username = StringField("New username.", validators=[Optional(), Length(max=50)])
    name = StringField("Your name", validators=[Optional(), Length(max=100)])
    location = StringField("Where are you from.", validators=[DataRequired(), Length(max=100)])
    about_me = TextAreaField("Say something about yourself.", validators=[Optional(), Length(max=80)])

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if field.data != self.username and user:
            raise ValidationError('Username already in use.')


class feedback(FlaskForm):
    feed = TextAreaField("What didn't go right?, tell us.", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Send")


class SearchQuery(FlaskForm):
    where = StringField("where to?", validators=[DataRequired()])
    adults = IntegerField("total adults", validators=[DataRequired(), NumberRange(min=0, max=100)])
    kids = IntegerField("total kids", validators=[Optional(), NumberRange(min=0, max=100)])
    checkin = DateField("start date", validators=[DataRequired()])
    checkout = DateField("end date", validators=[DataRequired()])
    rooms = IntegerField("preferred number of rooms", validators=[Optional(), NumberRange(min=1, max=5)])
