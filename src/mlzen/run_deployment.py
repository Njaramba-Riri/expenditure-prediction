import click

from rich import print
from typing import cast

from zenml.integrations.mlflow.model_deployers.mlflow_model_deployer import MLFlowModelDeployer
from zenml.integrations.mlflow.services import MLFlowDeploymentService
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri

from pipelines.deploy.deployment_pipeline import continous_deployment_pipeline, inference_pipeline

DEPLOY = "deploy"
PREDICT = "predict"
DEPLOY_AND_PREDICT = "deploy_and_predict"

@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Choice([DEPLOY, PREDICT, DEPLOY_AND_PREDICT]),
    default=DEPLOY_AND_PREDICT,
    help="You can only choose to run the deployment pipeline which will trigger \
          train and deployment of the model ('deploy'), or to run a prediction on the model ('predict'). \
            By default both deployment and prediction will run, ('deploy_and_predict')."
)

@click.option(
    "--min-accuracy",
    default=0,
    help="Mininum accuracy required to deploy the model."
)

def run_deployment(config: str, min_accuracy: float):
    mlflow_model_deployer_component = MLFlowModelDeployer.get_active_model_deployer()
    deploy = config == DEPLOY or config == DEPLOY_AND_PREDICT
    predict = config == PREDICT or config == DEPLOY_AND_PREDICT
    if deploy:
        continous_deployment_pipeline(
            data_path="Datasets/Train.csv",
            min_accuracy=min_accuracy,
            workers=3,
            timeout=60)
    if predict:
        inference_pipeline(
            pipeline_name="continous_deployment_pipeline",
            pipeline_step_name="mlflow_model_deployer_step"
        )

    print(
        "You can run:\n"
        f"[italic green] mlflow ui --backend-store-uri '{get_tracking_uri()}'[/italic green]\n"
        f"to inspect your experiment runs within the MLFlow UI. "
    )

    existing_services = mlflow_model_deployer_component.find_model_server(
        pipeline_name="continuous_deployment_pipeline",
        pipeline_step_name="mlflow_model_deployer_step",
        model_name="model"
    )

    if existing_services:
        service = cast(MLFlowDeploymentService, existing_services[0])
        if service.is_running:
            print(
                f"The MLFlow prediction server is running locally as a daemon"
                f"process service and accepts inference requests at:\n"
                f"  {service.prediction_url}\n"
                f"To stop the service, run "
                f"[italic green] `zenml model-deployer models delete"
                f"{str(service.uuid)}`[/italic green]."
            )
        elif service.is_failed:
            print(
                f"The MLFlow prediction server is in a failed state:\n"
                f" Last state: '{service.status.state.value}'\n"
                f" Last error: '{service.status.last_error}' "
            )
    else:
        print(
            "No MLFlow prediction server is currently running. \
                The deployment pipeline must be run first to train and deploy the model. \
                    Execute the same command with the `--deploy` argument to deploy it."
        )


if __name__ == "__main__":
    run_deployment()