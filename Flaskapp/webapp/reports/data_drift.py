import datetime

import numpy as np
import pandas as pd

from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, ColumnSummaryMetric
from evidently.metrics import DatasetDriftMetric, DatasetMissingValuesMetric

from evidently.ui.workspace import WorkspaceBase, Workspace

def drift_report(i: int):
    report = Report(
        metrics=[
            DatasetDriftMetric(),
            DatasetMissingValuesMetric(),
            ColumnDriftMetric(column_name="total_male", stattest="wasserstein"),
            ColumnSummaryMetric(column_name="total_male"),
            ColumnDriftMetric(column_name="night_mainland", stattest="wasserstein"),
            ColumnSummaryMetric(column_name="night_mailand")
        ],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i)
    )

    report.run(reference_data="", current_data="")
    return report

def create_reports(workspace: str):
    ws = Workspace.create(workspace)
    

if __name__ == "__main__":
    create_reports(WORKSPACE)