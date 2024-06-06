import os
import warnings
import pickle
import datetime
warnings.filterwarnings("ignore")

import pandas as pd

import evidently
from evidently.report import Report
from evidently.metrics import DatasetSummaryMetric, ColumnDriftMetric, ColumnMissingValuesMetric
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics.base_metric import generate_column_metrics
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import *
from evidently.test_preset import DataDriftTestPreset
from evidently.test_suite import TestSuite
from evidently.tests.base_test import generate_column_tests
from evidently.test_preset import DataQualityTestPreset, DataStabilityTestPreset
from evidently.tests import *
from evidently.ui.dashboards import CounterAgg, PlotType, PanelValue
from evidently.ui.dashboards import DashboardPanelCounter, DashboardPanelPlot
from evidently.test_preset import MulticlassClassificationTestPreset


from evidently.report import Report
from evidently.metrics import *

from evidently.test_preset import DataDriftTestPreset
from evidently.test_suite import TestSuite
from evidently import ui
from evidently.ui.dashboards import CounterAgg
from evidently.ui.dashboards import DashboardPanelCounter
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.dashboards import ReportFilter
from evidently.ui.remote import RemoteWorkspace
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase


expend = pd.read_csv("~/Desktop/expenditure/Datasets/Train.csv")
expend.drop("Tour_ID", axis=1, inplace=True)
expend_ref = expend[~expend.cost_category.isin(["Higher Cost", "Lower Cost", "Highest Cost"])]
expend_cur = expend[expend.cost_category.isin(["Higher Cost", "Lower Cost", "Highest Cost"])]

WORKSPACE = "expenditure"
PROJECT_NAME = "Tourist Expenditure Prediction"
PROJECT_DESCRIPTION = "Leveraging the power of ML to uncover the underlying patterns that influence tourist    spending."


def create_report(i: int):
    data_drift_report = Report(
        metrics=[
            DatasetDriftMetric(),
            DatasetMissingValuesMetric(),
            ColumnDriftMetric(column_name="total_male", stattest="wasserstein"),
            ColumnSummaryMetric(column_name="total_male"),
            ColumnDriftMetric(column_name="purpose", stattest="wasserstein"),
            ColumnSummaryMetric(column_name="purpose"),
        ],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i),
    )

    data_drift_report.run(reference_data=expend_ref, current_data=expend_cur.iloc[100 * i : 100 * (i + 1), :])
    return data_drift_report


def create_test_suite(i: int):
    data_drift_test_suite = TestSuite(
        tests=[DataDriftTestPreset()],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i),
    )

    data_drift_test_suite.run(reference_data=expend_ref, current_data=expend_cur.iloc[100 * i : 100 * (i + 1), :])
    return data_drift_test_suite


def create_project(workspace: WorkspaceBase):
    #app = current_app._get_current_object()
    project = workspace.create_project(PROJECT_NAME)
    project.description = PROJECT_DESCRIPTION
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Tourist Spending Category",
        )
    )
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Model Calls",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetMissingValuesMetric",
                field_path=DatasetMissingValuesMetric.fields.current.number_of_rows,
                legend="count",
            ),
            text="count",
            agg=CounterAgg.SUM,
            size=1,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Share of Drifted Features",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetDriftMetric",
                field_path="share_of_drifted_columns",
                legend="share",
            ),
            text="share",
            agg=CounterAgg.LAST,
            size=1,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Dataset Quality",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(metric_id="DatasetDriftMetric", field_path="share_of_drifted_columns", legend="Drift Share"),
                PanelValue(
                    metric_id="DatasetMissingValuesMetric",
                    field_path=DatasetMissingValuesMetric.fields.current.share_of_missing_values,
                    legend="Missing Values Share",
                ),
            ],
            plot_type=PlotType.LINE,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="total_male: Wasserstein drift distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "total_male"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="Drift Score",
                ),
            ],
            plot_type=PlotType.BAR,
            size=1,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="purpose: Wasserstein drift distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "purpose"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="Drift Score",
                ),
            ],
            plot_type=PlotType.BAR,
            size=1,
        )
    )
    project.save()
    return project


def create_model_performance(workspace: str):
    ws = Workspace.create(workspace)
    project = create_project(ws)

    for i in range(0, 5):
        report = create_report(i=i)
        ws.add_report(project.id, report)

        test_suite = create_test_suite(i=i)
        ws.add_test_suite(project.id, test_suite)



if __name__ == "__main__":
    create_model_performance("Workspacee")
