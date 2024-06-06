import datetime

import pandas as pd

from flask import render_template

from evidently.test_suite import TestSuite
from evidently.tests.base_test import generate_column_tests
from evidently.test_preset import (DataDriftTestPreset, DataStabilityTestPreset, 
                                   DataQualityTestPreset, NoTargetPerformanceTestPreset)
from evidently.tests import *


reference = pd.read_csv("src/models/notebooks/classification/Version_1.csv")
reference.rename(columns={"cost_category": "target"}, inplace=True)

def create_tests(i: int, current: pd.DataFrame, reference=reference):
    suite = TestSuite(tests=[
        DataDriftTestPreset(cat_stattest='chisquare', cat_stattest_threshold=0.05),
        NoTargetPerformanceTestPreset(stattest_threshold=0.5)
    ],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i)
    )
    
    suite.run(reference_data=reference, current_data=current)
    
    another_path = "flaskapp/webapp/templates/reports/t-tests.html"
    
    suite.save_html(another_path)

    
    return render_template("/reports/t-tests.html")
