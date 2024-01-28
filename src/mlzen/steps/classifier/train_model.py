import logging
from typing import Tuple, Annotated, Union
import yaml 

import pandas as pd
import numpy as np

from sklearn.base import ClassifierMixin
from catboost.core import CatBoostClassifier

from zenml import step
from zenml.client import Client
import mlflow

from utils.classifier.model_train import RandomForest, CatBoost, XGBoost, LightGClassifier

experiment_tracker = Client().active_stack.experiment_tracker

with open('src/mlzen/steps/classifier/models.yml', 'r') as f:
    model_configs = yaml.safe_load(f)


@step(experiment_tracker=experiment_tracker.name)
def model_train(
    X_train: np.ndarray, 
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray
) -> Annotated[ClassifierMixin, "LGBM Classifier"]: 
    # Annotated[ClassifierMixin, "XGB classifier"],  
    # Annotated[ClassifierMixin, "forest classifier"],  
    # Annotated[CatBoostClassifier, "catboost classifier" ]
    
    """Model training step.

    Args:
        X_train (np.ndarray): Training features in form of numpy arrays.
        X_test (np.ndarray): Testing features in form of numpy arrays.
        y_train (np.ndarray): Training target variable in form of numpy array.
        y_test (np.ndarray): Testing target variable in form of numpy array.

    Returns:
        Union[ClassifierMixin, RegressorMixin, CatBoostClassifier, CatBoostRegressor]: 
    """
    try:
        model = None
        for model_config in model_configs["models"]:
            model_name = model_config["name"]
            model_parameters = model_config["parameters"]

            if model_name == "LGBMClassifier":
                model = LightGClassifier()
                mlflow.lightgbm.autolog()
                trained_lgb = model.train(X_train, y_train, **model_parameters)
            # elif model_name == "XGBClassifier":
            #     model = XGBoost()
            #     mlflow.xgboost.autolog()
            #     trained_xgb = model.train(X_train, y_train, **model_parameters)
            # elif model_name == "RandomForest":
            #     model = RandomForest()
            #     mlflow.sklearn.autolog()
            #     trained_forest = model.train(X_train, y_train, **model_parameters)
            # elif model_name == "CatBoost":
            #     model = CatBoost()
            #     trained_cat = model.train(X_train, y_train, **model_parameters)
            else:
                raise ValueError("Model {} not supported".format(model_name))
        return trained_lgb#, trained_xgb, trained_forest, trained_cat)
    except Exception as e:
        logging.error("Error while trying to train the model: {}".format(e))
        raise e

