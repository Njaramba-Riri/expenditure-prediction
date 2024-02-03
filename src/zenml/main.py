import click

from pipelines.local.regressor_pipeline import run_regressor
from pipelines.local.classifier_pipeline import run_classifier

from zenml.client import Client

if __name__ == "__main__":
    path = "Datasets/Train.csv"
    run_classifier.with_options(
        run_name="Expenditure classifier_{{date}}"
    )

    print(Client().active_stack.experiment_tracker.get_tracking_uri())
    run_classifier(data_path=path)
    run_regressor(data_path="Datasets/Train (1).csv")
    
    