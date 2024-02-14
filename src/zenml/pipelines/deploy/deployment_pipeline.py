import numpy as np
import pandas as pd
import json

from zenml import pipeline, step
from zenml.steps import BaseParameters
from zenml.config import DockerSettings
from zenml.integrations.constants import MLFLOW
from zenml.integrations.mlflow.steps import mlflow_model_deployer_step
from zenml.constants import DEFAULT_SERVICE_START_STOP_TIMEOUT

from steps.load_data import data_load
from steps.classifier.clean_data import data_cleaning
from steps.classifier.train_model import model_train
from steps.classifier.evaluate_model import model_evaluate
from steps.regressor.clean_data import data_clean
from steps.regressor.train_model import train_regressor
from steps.regressor.evaluate_model import evaluate_regressor

from .predict_steps import dynamic_importer, prediction_service_loader, predictor

docker_settings = DockerSettings(required_integrations=[MLFLOW])

class DeploymentTriggerConfig(BaseParameters):
    """Configuration trigger for the model deployment.

    Args:
        BaseParameters (_type_): _description_
    """
    min_accuracy: float = 0.0

class MLFlowDeploymentLoaderStepsParameters(BaseParameters):
    """MLFlow deployment getter parameters.

    Attributes:
        pipeline_name: Name of the pipeline that deployed MLFlow prediction server.
        step_name: Name of the step that deployed MLFlow prediction server.
        model_name: Name of the model that is deployed.
        running: If prediction server is running; defaults to `True`.
    """
    pipeline_name: str
    step_name: str
    model_name: str
    running: bool = True

@step
def deployment_trigger(accuracy: float,
                       config: DeploymentTriggerConfig):
    """Implements the configuration trigger that checks if the accuracy > min_accuracy for the deployment to happen.

    Args:
        accuracy (float): Model accuracy.
        config (DeploymentTriggerConfig): Configuration class with the actual config.
    
    Returns:
        Bool: True if the accuracy is >= min_accuracy, else False.
    """
    return accuracy > config.min_accuracy

@pipeline(name="Deployment Pipeline", enable_cache=False, settings={"docker": docker_settings})
def continous_deployment_pipeline(
    data_path: str,
    min_accuracy: float = 0.0,
    workers: int = 3,
    timeout: int = DEFAULT_SERVICE_START_STOP_TIMEOUT,
):
    df = data_load(data_path)
    X_train, X_test, y_train, y_test = data_cleaning(df)
    model = model_train(X_train, y_train, X_test, y_test)
    pre_score, rec_score, f1, roc_auc = model_evaluate(model, X_test, y_test)

    deployment_decision = deployment_trigger(roc_auc)
    mlflow_model_deployer_step(
        model = model,
        deploy_decision = deployment_decision,
        workers = workers,
        timeout = timeout
    )

@pipeline(name="Inference Pipeline", enable_cache=False, settings={"docker": docker_settings})
def inference_pipeline(pipeline_name: str, 
                       pipeline_step_name: str,
                       model_name: str):
    data = dynamic_importer()
    service = prediction_service_loader(
        pipeline_name=pipeline_name,
        pipeline_step_name=pipeline_step_name,
        model_name=model_name,
        running=False
    )
    prediction = predictor(service=service, data=data)
    return prediction