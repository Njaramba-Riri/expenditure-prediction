from flask import Blueprint, flash, url_for, render_template, redirect
from flask_login import login_required 

import pandas as pd

from ..auth import admin_required, has_role, permission_required
from ..mainapp.models import Features
from .report import create_report
from .suites import create_tests

reports_blueprint = Blueprint("report", __name__, 
                              url_prefix="/letsgo/admin/reports")

def get_features():
    data = Features.query.all()
    data_dict = {column.name: [getattr(row, column.name) for row in data] for column in Features.__table__.columns}
    data_df = pd.DataFrame(data_dict)
    
    return data_df

@reports_blueprint.route("/")
@login_required
@admin_required
def show_report():
    current = get_features()
    current.rename(columns={
                            "sub_region": "sub-region"}, inplace=True)
    current['travel_with'].rename({"Alone": "Alone"}, inplace=True)
    current['cost_category'] = current['predicted_category']
    current = current.drop(columns=['user_id', 'total_cost', 'probability'], axis=1)
    
    path = create_report(current=current)
    
    return render_template("/reports/report.html", visuals=path)

@reports_blueprint.route("/tests")
@login_required
@admin_required
def show_tests():
    current = get_features()
    current.rename(columns={"predicted_category": "target",
                            "sub_region": "sub-region"}, inplace=True)
    current = current.drop(columns=['user_id', 'total_cost', 'date', 'id', 'probability'], axis=1)
    
    path = create_tests(i=10, current=current)
    
    return render_template("/reports/tests.html", suites=path)
