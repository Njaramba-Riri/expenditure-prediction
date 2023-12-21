from flask import Blueprint, redirect, url_for, render_template, request, flash, abort, session, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from flask_moment import Moment
import requests
from flask_jwt_extended import create_access_token

from .models import User
from .forms import user_register, user_signin, forgot, ResetPassword, changePass 

from ..email import send_email

from .. import db
from . import authenticate

auth_blueprint = Blueprint("auth", __name__,
                           static_folder="../static/auth/",
                           template_folder="../templates/auth", 
                           url_prefix= "/letsgo/auth")

@auth_blueprint.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth_blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('app.index'))
    return render_template('auth/unconfirmed.html')

@auth_blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    form = user_signin()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for('app.index')
            return redirect(next_url)
        flash("Invalid username or password")
    return render_template('auth/user_login.html', form=form) 

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = user_register()
    if request.method == 'POST' and form.validate():
        new_user = User()
        new_user.email = form.email.data.lower()
        new_user.username = form.username.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirmation_token()
        send_email(new_user.email, "Confirm your account.",
                    "auth/email/confirm", user=new_user, token=token)
        flash("A confirmation email has been sent to you.", category="info")
        return redirect(url_for('.signin'))
    return render_template('auth/register.html', form=form)

@auth_blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('app.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Welcome to the party!.')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('app.index'))


@auth_blueprint.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email, kindly check your inbox.')
    return redirect(url_for('app.index'))

@auth_blueprint.route('/<username>/change_password', methods=['GET', 'POST'])
@login_required
def changePassword(username):
    form = changePass()
    user = User.query.filter_by(username=username).first()
    if form.validate_on_submit():
        if user.check_password(form.old_password.data):
            user.password = user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()
            flash("Password changed successfully, you'll be redirected to login page.")
            logout_user()
            return redirect(url_for('auth.signin'))
        else:
            flash("Invalid password.")
    return render_template('/auth/changepass.html', form=form)

@auth_blueprint.route('/reset', methods=['GET', 'POST'])
def forgotpass():
    if not current_user.is_anonymous:
        redirect(url_for('app.index'))
    form = forgot()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/resetpass', user=user, token=token)
        flash("An email with reset instructions has just been sent to you.")
        return redirect(url_for('.signin'))
    return render_template('/auth/forgot.html', form=form)

@auth_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('app.index'))
    form = ResetPassword()
    if form.validate_on_submit():
        if User.confirm_reset_token(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')    
            return redirect(url_for('signin'))
        else:
            return redirect(url_for('app.index'))
    return render_template('/auth/changepass.html', form=form)

@auth_blueprint.route('/api', methods=['POST'])
def api():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = authenticate(username, password)
    if not user:
        return jsonify({"msg": "Invalid credentials."})
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@auth_blueprint.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("You've logged out. ", category="info")
    return redirect(url_for('app.index'))
