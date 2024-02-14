import os 
import pickle
import random
import json

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from flask import (Blueprint,render_template, redirect, url_for, 
                   flash, session, request, jsonify, current_app, abort)
from flask_login import login_required, current_user
from sqlalchemy import exc

from ..reports.model_performance import create_model_performance
from ..reports.data_drift import drift_report
from ..reports.featured import plot_categorical, create_plots

from webapp import db
from ..auth import has_role, permission_required, admin_required
from ..auth.models import User, Role
from ..mainapp.models import Features, Feedback
from .models import Admin
from .forms import editAdmin, editProfile



admin_blueprint = Blueprint('admin', __name__,
                            static_folder='../static/admin',
                            template_folder='../templates/admin',
                            url_prefix="/letsgo/admin"
                            )

dire = os.path.dirname(__file__)
model = pickle.load(open(os.path.join(dire, "pickle_objects", "Cat.pkl"), 'rb'))
senti_clf = pickle.load(open(os.path.join(dire, "pickle_objects", "classifier.pkl"), 'rb'))


def fetch_data():
    results = Features.query.all()
    return [{column.name: getattr(row, column.name) for column in row.__table__.columns} for row in results]

@admin_blueprint.route("/")
@login_required
@admin_required
def admindashboard():
    all_u = User.query.all()
    users = random.sample(all_u, min(3, len(all_u)))
    feedback = Feedback.query.all()
    feedback = random.sample(feedback, min(5, len(feedback))) 
    features = Features.query.order_by(Features.date.desc()).all()
    features = random.sample(features, min(5, len(features)))
    late_feed = Feedback.query.order_by(Feedback.date.desc()).limit(10).all()
    return render_template('dashboard.html', users=users, all=all_u, 
                           feedback=feedback, features=features, feed=late_feed)

@admin_blueprint.route("/features", methods=['GET', 'POST'])
@login_required
@admin_required
def fetch_features():
    result = fetch_data()
    return jsonify(result)

@admin_blueprint.route("/users", methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.last_seen.desc())
    pagination = db.paginate(users, page=page, per_page=7, error_out=False)
    users = pagination.items
    return render_template("admin/users.html", users=users, pagination=pagination)

@admin_blueprint.route("/feedback")
@login_required
@admin_required
def feed():
    users = User.query.all()
    feat = Features.query.all()
    page = request.args.get('page', 1, type=int)
    feed = Feedback.query.order_by(Feedback.date.desc())
    pagination = db.paginate(feed, page=page, per_page=10, error_out=False)
    feedback = pagination.items
    return render_template("admin/feedback.html", feedback=feedback, pagination=pagination, 
                           features=feat, users=users ,zip=zip)
@admin_blueprint.route("/all_features")
@login_required
@admin_required
def features():
    feats = Features.query.order_by(Features.date.asc()).order_by(Features.id.asc())
    page = request.args.get('page', 1, type=int)
    pagination = db.paginate(feats, page=page, per_page=10, error_out=False)
    feats = pagination.items

    return render_template("admin/features.html", features=feats, pagination=pagination)

@admin_blueprint.route('/profile_edit/<username>/', methods=['GET', 'POST'])
@login_required
@admin_required
def update_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No such user exists", 'info')
        return redirect(url_for('.users'))
    form = editProfile(user=user)
    if request.method == 'POST' and form.validate_on_submit():
        user.email = form.email.data
        user.full_name = form.name.data
        user.username = form.username.data
        user.mobile = form.mobile.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about = form.about.data
        user.confirmed = form.confirmed.data
        try:
            db.session.add(user)
            db.session.commit()
            flash('User details updated successfully.', category="info")
            return redirect(url_for('.users'))
        except Exception:
            db.session.rollback()
            flash("User details not updated.", 'info')
    return render_template('/user/editProfile.html', form=form, user=user)

@admin_blueprint.route("/<string:username>/admin-profile/")
@login_required
@admin_required
def profile(username):
    user = User.query.filter_by(username=username).first() or \
        Admin.query.filter_by(username=username).first()
    if not user:
        flash("User not found or user is not an adminstrator", category="warning") 
    return render_template("admin/profile.html", user=user)


@admin_blueprint.route("/profile/edit/<string:username>", methods=['POST', 'GET'])
@login_required
@admin_required
def edit_admin(username):
    user = Admin.query.filter_by(username=username).first() 
    if not user:
        user = User.query.filter_by(username=username).first_or_404()
    if not user.is_administrator():
        return redirect(url_for('.user_profile', username=user.username))
    form = editAdmin()
    if form.validate_on_submit():
        admin = Admin()

        admin.name = form.name.data
        #admin.email = form.email.data
        admin.username = form.username.data
        admin.mobile = form.mobile.data
        admin.agency = form.agency.data
        admin.agency_email = form.agency_email.data
        admin.agency_mobile = form.agency_mobile.data
        admin.agency_address = form.agency_address.data
        try:
            db.session.add(admin)
            db.session.commit()
            flash("Adminstrator profile details updated succesfully", category="info")
            return redirect(url_for('.profile', username=admin.username))
        except BaseException as e:
            db.session.rollback()
            flash("Adminstrator profile not updated!: {}".format(e), category="warning")
            return redirect(url_for('.profile', username=user.username))
    return render_template("admin/editadmin.htm", form=form, user=user)

@admin_blueprint.route('/user_profile/<username>/', methods=['GET', 'POST'])
@login_required
@admin_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No such user with the given username', 'warning')
        return redirect(url_for('.users')) 
       
    return render_template('/user/view.html', user=user)

@admin_blueprint.route('/remover_user/<username>/', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        try: 
            db.session.delete(user)
            db.session.commit()
            flash(f"User {user.username} removed successfully", category="info")
            return redirect(url_for('.users'))
        except Exception:
            db.session.rollback()
            flash("User couldn't be removed.", 'info')
            return redirect(url_for('.users'))
    else:
        flash("User with such username not found", category='warning')
        return redirect(url_for('.users'))

@admin_blueprint.route("/reports")
@login_required
def reports():
    return render_template("admin/reportsdash.html")

@admin_blueprint.route("reports/model_performance")
@login_required
def performance():
    report = create_model_performance(workspace="expenditure")
    return report


@admin_blueprint.route("reports/featured")
@login_required
def featured_visuals():
    bar = create_plots()
    return render_template("reports/featured.html", repo=bar)

@admin_blueprint.route('/matrix')
@login_required
def matrix():
    original = pd.read_csv("../Datasets/train.csv")
    y = original['cost_category']

    le = LabelEncoder()
    y = le.fit_transform(y)

    X = Features.query.filter_by(Features.id).all()
    y_true = y
    y_pred  = model.predict(X)
    cm = confusion_matrix(y_true=y_true, y_pred=y_pred)
    sns.heatmap(cm, annot=True, format='g', cbar=True, 
                xticklabels=le.classes_, yticklabels=le.classes_)

    return "This is Matrix"

@admin_blueprint.route("/generalization")
@login_required
@admin_required
def report():
    #X_test = [np.random.random_integers(1)]
    #y_pred = model.predict(X_test)
    y_true = [np.random.random_sample(50000)]
    y_pred = [np.random.random_sample(50000)]
    res = mean_squared_error(y_true, y_pred)
    return jsonify(res)

@admin_blueprint.route("/featured")
@login_required
@admin_required
def visuals():
    return "This is the intended Visualization page."

