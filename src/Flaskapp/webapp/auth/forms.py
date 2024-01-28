import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp

from .models import User

class user_register(FlaskForm):
    email = StringField("Enter your email. ", validators=[DataRequired(), Length(max=64) , 
                                                          Email(message="Kindly check your email address.")])
    username = StringField("Your preffered username. ", validators=[DataRequired(), Length(max=64),
                                                      Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, \
                                                             'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField("Your password. ", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField("Confirm password. ", validators=[DataRequired(), 
                                                              EqualTo('password', message="Passwords must match.")])
    #captcha = RecaptchaField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already exists.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")


class user_signin(FlaskForm):
    username = StringField("Enter username. ", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Your password. ", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in.")
    
    def validate(self, extra_validators=None):
        check_validate =  super(user_signin, self).validate(extra_validators)
        if not check_validate:
            return False
        #User exists?
        user =  User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append("User with that username doesn't exist.")
            return False
        #check password match
        if not user.check_password(self.password.data):
            self.password.errors.append("Username and password didn't match.")
            return False
        return True

    
class changePass(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=8)])
    confirm= PasswordField('Confirm new password', validators=[DataRequired(), 
                                                               EqualTo('confirm', message='Passwords must match.')])


class forgot(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    
    def validate_email(self, field):
        # Check if email is valid
        if not re.match(r"[^@]+@[^@]+\.[^@]+", field.data):
            raise ValidationError("Enter a valid email.")
        
        # Check if email exists in the database
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError("User with that email doesn't exist.")


class ResetPassword(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), 
                                                         EqualTo('confirm', message='Passwords must match!.')])
    confirm = PasswordField('Confirm password', validators=[DataRequired()])

