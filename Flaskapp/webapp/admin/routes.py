from flask import render_template, url_for, Blueprint, flash, redirect, session, request, jsonify
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
model = pickle.load(open(os.path.join(dire, "pickle_objects", "cat.pkl"), 'rb'))
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

@admin_blueprint.route("/dashboard")
@login_required
@admin_required
def admindashboard():
    user = User.query.order_by(User.id).all()
    users = User.query.all()
    users = random.sample(users, min(3, len(users)))
    feedback = Feedback.query.all()
    feedback = random.sample(feedback, min(3, len(feedback))) 
    features = Features.query.order_by(Features.date.desc()).limit(10)
    #features = random.sample(features, min(3, len(features)))
    return render_template('dashboard.html', users=users, feedback=feedback, features=features, user=user)


@admin_blueprint.route('/profile_edit/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def update_profile(id):
    user = User.query.get_or_404(id)
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

        db.session.add(user)
        flash('User details updated successfully.')
        return redirect(url_for('.admindashboard'))
    return render_template('/auth/editProfile.html', form=form, user=user)

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

@admin_blueprint.route("/feedback")
@login_required
@admin_required
def feedback():
    return render_template("admin/feeddash.html")

@admin_blueprint.route("all_feedback")
@login_required
@admin_required
def feed():
    usermodel = User
    feedmodel = Feedback
    featuremodel = Features
    feed = Feedback.query.all()
    feat = Features.query.all()
    return render_template("admin/feedback.html", feedback=feed, 
                           feature=feat, feedmodel=feedmodel, 
                           featuremodel=featuremodel, usermodel=usermodel, zip=zip)

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

@admin_blueprint.route("users", methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    form = UsersForm()
    if request.method == 'POST' and form.validate_on_submit():
        users_email = User.query.filter_by(email=form.user.data).first_or_404()
        users_id = User.query.filter_by(id=form.user_id.data).first_or_404()
        #resp = json.loads(users_email)
        return jsonify({"User": users_email.id})
    return render_template("admin/users.html",form=form)
