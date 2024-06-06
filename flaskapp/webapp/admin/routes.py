import os 
import pickle
import random
import datetime
from datetime import datetime, timedelta
import base64
import io

from flask import (Blueprint,render_template, redirect, url_for, 
                   flash, session, request, jsonify, current_app, abort)
from flask_login import login_required, current_user
from sqlalchemy import exc

import pandas as pd
import matplotlib.pyplot as plt

from webapp import db
from ..auth import has_role, permission_required, admin_required
from ..auth.models import User, Role
from ..mainapp.models import Features, Feedback
from .models import Admin
from .forms import editAdmin, editProfile
from ..reports.utils import get_model_score 


admin_blueprint = Blueprint('admin', __name__,
                            static_folder='../static/admin',
                            template_folder='../templates/admin',
                            url_prefix="/letsgo/admin"
                            )

dire = os.path.dirname(__file__)
model = pickle.load(open(os.path.join(dire, "pickle_objects", "Cat_v3.pkl"), 'rb'))
senti_clf = pickle.load(open(os.path.join(dire, "pickle_objects", "classifier.pkl"), 'rb'))
importance = pd.read_csv("/home/riri/Desktop/expenditure/src/models/notebooks/classification/Importances.csv")
imps = importance.to_dict(orient='records')
importance.plot(kind='barh')
plt.xlabel('Importance')
plt.ylabel('Features')
plt.title('Feature Importance')

img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)

plot_url = base64.b64encode(img.getvalue()).decode()

def fetch_data():
    results = Features.query.all()
    return [{column.name: getattr(row, column.name) for column in row.__table__.columns} for row in results]

@admin_blueprint.route("/features", methods=['GET', 'POST'])
@login_required
@admin_required
def fetch_features():
    result = fetch_data()
    return jsonify(result)

@admin_blueprint.route("/")
@login_required
@admin_required
def admindashboard():
    date_from = datetime.now() - timedelta(days=90)
    all_u = User.query.all()
    new = User.query.filter(User.date_created > date_from).all()
    users = random.sample(all_u, min(3, len(all_u)))
    feedback = Feedback.query.all()
    feedback = random.sample(feedback, min(5, len(feedback))) 
    features = Features.query.order_by(Features.date.desc()).all()
    feats = random.sample(features, min(5, len(features)))
    late_feed = Feedback.query.order_by(Feedback.date.desc()).limit(10).all()
    return render_template('dashboard.html', users=users, all=all_u, 
                           score=get_model_score(), new=new, model=model, 
                           feedback=feedback, features=feats, all_f=features,
                           feed=late_feed, imps=imps, plot=plot_url)
    
@admin_blueprint.route("/users", methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    features = Features.query.all()
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.last_seen.desc())
    pagination = db.paginate(users, page=page, per_page=7, error_out=False)
    users = pagination.items
    return render_template("admin/users.html", users=users, 
                           pagination=pagination, features=features)

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
                           features=feat, users=users, zip=zip, enumerate=enumerate)
@admin_blueprint.route("/all_features")
@login_required
@admin_required
def features():
    users = User.query.all()
    feats = Features.query.order_by(Features.date.asc()).order_by(Features.id.asc())
    page = request.args.get('page', 1, type=int)
    pagination = db.paginate(feats, page=page, per_page=10, error_out=False)
    feats = pagination.items

    return render_template("admin/features.html", features=feats, 
                           pagination=pagination, users=users)

@admin_blueprint.route("/<string:username>/admin-profile/")
@login_required
@admin_required
def profile(username):
    user = Admin.query.filter_by(username=username).first() or User.query.filter_by(username=username).first()
    if not user:
        flash("User not found or user is not an administrator", category="warning") 
    return render_template("admin/profile.html", user=user)


@admin_blueprint.route("/<string:username>/admin-profile/update", methods=['POST', 'GET'])
@login_required
@admin_required
def edit_admin(username):
    user = Admin.query.filter_by(username=username).first_or_404() 
    if not user:
        user = User.query.filter_by(username=username).first()
    if not user.is_administrator():
        return redirect(url_for('.user_profile', username=user.username))
    form = editAdmin()
    if form.validate_on_submit():
        admin = Admin()

        admin.name = form.name.data
        admin.email = form.email.data
        admin.username = user.username
        admin.mobile = form.mobile.data
        admin.agency = form.agency.data
        admin.agency_email = form.agency_email.data
        admin.agency_mobile = form.agency_mobile.data
        admin.agency_address = form.agency_address.data
        try:
            db.session.add(admin)
            db.session.commit()
            flash("Administrator profile details updated succesfully", category="info")
            return redirect(url_for('.user_profile', username=user.username))
        except BaseException as e:
            db.session.rollback()
            flash("Administrator profile not updated!: {}".format(e), category="warning")
            return redirect(url_for('.profile', username=current_user.username))
    
    form.name.data = user.name
    form.email.data = user.email
    form.agency.data = user.agency
    form.mobile.data = user.mobile
    form.agency_email.data = user.agency_email
    form.agency_address.data = user.agency_address
    form.agency_mobile.data = user.agency_mobile
    
    return render_template("admin/editadmin.html", form=form, user=user)

@admin_blueprint.route('/<string:username>@user-profile', methods=['GET', 'POST'])
@login_required
@admin_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No such user with the given username', 'warning')
        return redirect(url_for('.users')) 
    
    return render_template('/user/view.html', user=user)

@admin_blueprint.route('/@<string:username>/user-profile/update', methods=['GET', 'POST'])
@login_required
@admin_required
def update_profile(username):
    user = Admin.query.filter_by(username=username).first() or User.query.filter_by(username=username).first()
    if not user:
        flash("User with that such username doesn't exist!.", "warning")
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
            return redirect(url_for('.user_profile', username=user.username))
        except Exception:
            db.session.rollback()
            flash("User details not updated.", 'info')
    
    form.email.data = user.email
    form.name.data = user.full_name
    form.username.data = user.username
    form.role.data = user.role
    form.location.data = user.location
    form.about.data = user.about
    form.confirmed.data = user.confirmed
    
    return render_template('/user/editProfile.html', form=form, user=user)

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
