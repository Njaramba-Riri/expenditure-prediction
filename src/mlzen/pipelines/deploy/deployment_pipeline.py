import numpy as np
import pandas as pd
import json


from zenml import step, pipeline
from zenml.config import DockerSettings
from zenml.integrations.constants import MLFLOW
from zenml.constants import DEFAULT_SERVICE_START_STOP_TIMEOUT

from steps.load_data import data_load
from steps.classifier.clean_data import data_cleaning
from steps.classifier.train_model import model_train
from steps.classifier.evaluate_model import model_evaluate
from steps.regressor.clean_data import data_clean
from steps.regressor.train_model import train_regressor
from steps.regressor.evaluate_model import evaluate_regressor

from deploy_steps import deployment_trigger, dynamic_importer, \
      prediction_service_loader, predictor, mlflow_model_deployer_step

docker_settings = DockerSettings(required_integrations=[MLFLOW])

@pipeline(name="Deployment Pipeline", enable_cache=False, settings={"docker": docker_settings})
def continous_deployment_pipeline(
    data_path: str,
    min_accuracy: float =  0.50,
    workers: int = 1,
    timeout: int = DEFAULT_SERVICE_START_STOP_TIMEOUT,
):
    df = data_load(data_path)
    X_train, X_test, y_train, y_test = data_cleaning(df)
    models = model_train(X_train, y_train, X_test, y_test)
    for model in models:
        pre_score, rec_score, roc_auc, f1 = model_evaluate(model, X_test, y_test)

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