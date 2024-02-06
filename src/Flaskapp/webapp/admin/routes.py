from flask import render_template, url_for, Blueprint, flash, redirect, session, request, jsonify, current_app, abort
from .forms import UsersForm, editProfile
from ..auth.models import User, Role
from ..mainapp.models import Features, Feedback
from flask_login import login_required, logout_user, current_user
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from ..auth import has_role, permission_required, admin_required
from webapp import db

from ..reports.model_performance import create_model_performance
from ..reports.data_drift import drift_report
from ..reports.featured import plot_categorical, create_plots
#from webapp.app.routes import model 
import json
import random

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import sklearn
import pickle 
import os

admin_blueprint = Blueprint('admin', __name__,
                            static_folder='../static/admin',
                            template_folder='../templates/admin',
                            url_prefix="/letsgo/admin"
                            )

dire = os.path.dirname(__file__)
model = pickle.load(open(os.path.join(dire, "pickle_objects", "Cat.pkl"), 'rb'))
senti_clf = pickle.load(open(os.path.join(dire, "pickle_objects", "classifier.pkl"), 'rb'))


class CustomView(BaseView):
    @expose('/')
    @login_required
    @admin_required
    def index(self):
        return self.render('admin/custom.html')
    
    @expose('/reports')
    @login_required
    @admin_required
    def reports(self):
        return self.render('admin/reportsdash.html')

class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and \
        current_user.is_administrator()
    pass

class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and \
        current_user.is_administrator()
    pass


@admin_blueprint.route('/')
def home():
    """Landing page."""
    return render_template('/reports/featured.html',
                           title='Plotly Dash & Flask Tutorial',
                           template='home-template',
                           body="This is a homepage served with Flask.")

def fetch_data():
    results = Features.query.all()
    return [{column.name: getattr(row, column.name) for column in row.__table__.columns} for row in results]


@admin_blueprint.route("/features", methods=['GET', 'POST'])
@login_required
@admin_required
def fetch_features():
    result = fetch_data()
    return jsonify(result)

@admin_blueprint.route("/dashboard")
@login_required
@admin_required
def admindashboard():
    user = User.query.order_by(User.id).all()
    users = User.query.all()
    authenticated = [ user for user in users if user.confirmed ]
    anonymous = [ user for user in users if user.is_anonymous ]
    unverified = [ user for user in users if not user.confirmed ]   
    users = random.sample(users, min(5, len(users)))
    feedback = Feedback.query.all()
    feedback = random.sample(feedback, min(5, len(feedback))) 
    features = Features.query.order_by(Features.date.desc()).all()
    features = random.sample(features, min(5, len(features)))
    return render_template('dashboard.html', users=users, 
                           feedback=feedback, features=features,
                           auth=authenticated, anony=anonymous, unveri=unverified)

@admin_blueprint.route("/users", methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.last_seen.desc())
    pagination = db.paginate(users, page=page, per_page=7, error_out=False)
    users = pagination.items
    return render_template("admin/users.html",users=users, pagination=pagination)

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
        user.username = form.username.data
        user.mobile = form.mobile.data
        user.name = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about = form.about.data
        user.tour_company = form.company.data
        user.company_email = form.c_email.data
        user.company_mobile = form.c_mobile.data
        user.company_address = form.c_address.data
        user.confirmed = form.confirmed.data
        try:
            db.session.add(user)
            db.session.commit()
            flash('User details updated successfully.')
            return redirect(url_for('.users'))
        except Exception:
            db.session.rollback()
            flash("User details not updated.", 'info')
    return render_template('/user/editProfile.html', form=form, user=user)

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
            return redirect(url_for('.users'))
        except Exception:
            db.session.rollback()
            flash("User couldn't be removed.", 'info')
            return redirect(url_for('.users'))
    else:
        flash("User with such username not found", 'warn')
        return redirect(url_for('.users'))

@admin_blueprint.route("reports")
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

@admin_blueprint.route("/roc")
@login_required
def roc():

    return "This is roc"

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

@admin_blueprint.route("/profile")
@login_required
@admin_required
def profile():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template("admin/profile.html", user=user)
