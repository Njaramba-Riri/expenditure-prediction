import logging

from typing import Tuple
from typing_extensions import Annotated

import pandas as pd
import numpy as np
import json

from zenml import step
from zenml.integrations.mlflow.model_deployers.mlflow_model_deployer import MLFlowModelDeployer
from zenml.integrations.mlflow.services.mlflow_deployment import MLFlowDeploymentService

from .utils import get_data_for_test

@step(name="Data Loader", enable_cache=True)
def dynamic_importer() -> json:
    data = get_data_for_test()
    return data

@step(name="Check Prediction Service", enable_cache=False)
def prediction_service_loader(
    pipeline_name: str,
    pipeline_step_name: str,
    model_name: str,
    running: bool = True,
) -> MLFlowDeploymentService:
    """Gets the deployment service started by the deployment service.

    Args:
        pipeline_name (str): Name of the pipeline that deployed the MLFlow prediction server.
        pipeline_step_name (str): Name of the step that deployed the MLFlow prediction server.
        model_name (str): Name of the model that is deployed. Defaults to "model".
        running (bool, optional): Checks if there's a running service. Defaults to True.

    Returns:
        MLFlowDeploymentService: Daemon service.
    """
    #Get MLFlow deployer stack component.
    mlflow_model_deployer_component = MLFlowModelDeployer.get_active_model_deployer()

    #Fetch existing services with the pipeline, step, and model names.
    existing_services = mlflow_model_deployer_component.find_model_server(
        pipeline_name=pipeline_name,
        pipeline_step_name=pipeline_step_name,
        model_name=model_name,
        running=running
    )

    if not existing_services:
        RuntimeError(
            f"No MLFlow deployment service found for pipeline {pipeline_name},"
            f"step {pipeline_step_name}, and model {model_name}."
            f"Pipeline for the {model_name} model is currently running."
        )

    return existing_services[0]

@step(name="Prediction")
def predictor(
    service: MLFlowDeploymentService,
    data: str
) -> Tuple[
    Annotated[np.ndarray, "Total Cost"],
    Annotated[str, "Cost Category"]
]:
    service.start(timeout=5)
    pre_data = json.loads(data)
    pre_data.pop("columns")
    pre_data.pop("index")
    columns = [
        "country",
        "age_group",
        "travel_with",
        "total_male",
        "total_female",
        "purpose",
        "main_activity"
    ]
    df = pd.DataFrame(pre_data["data"], columns=columns)
    json_list = json.loads(json.dumps(list(df.T.to_dict().values)))
    pre_data = np.array(json_list)
    prediction = service.predict(pre_data)
    return prediction