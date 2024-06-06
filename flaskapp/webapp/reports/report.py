import datetime

import pandas as pd

from flask import render_template

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics.base_metric import generate_column_metrics
from evidently.metric_preset import (DataDriftPreset, DataQualityPreset, 
                                     TargetDriftPreset, ClassificationPreset)
from evidently.metrics import *

reference = pd.read_csv("src/models/notebooks/classification/Version_1.csv")
reference['predicted_category'] = reference['cost_category']
# reference.rename(columns={"cost_category": "target"}, inplace=True)

def create_report(current: pd.DataFrame, reference=reference):
    """Create monitoing reports.

    Args:
        current (pd.DataFrame): 
        reference (_type_, optional): Reference dataset to compare the current dataset to. Defaults to reference.

    Returns:
        _type_: HTML generated reports.
    """
    column_mapping = ColumnMapping()
    
    column_mapping.target = 'cost_category'
    column_mapping.prediction = 'predicted_category'
    column_mapping.numerical_features = ['night_mainland', 'night_zanzibar', 'duration']
    # column_mapping.datetime = 'date'
    # column_mapping.user_id = 'user_id'
    # column_mapping.id = 'id'
    
    
    report = Report(
        metrics=[
            DataDriftPreset(cat_stattest='chisquare', cat_stattest_threshold=0.05),
            ClassificationPreset(), 
            DataQualityPreset()
        ]
    )
    
    report.run(reference_data=reference, current_data=current, column_mapping=column_mapping)
    
    path = "flaskapp/webapp/templates/reports/generate.html"
    report.save_html(path)
    
    return render_template("reports/generate.html")
