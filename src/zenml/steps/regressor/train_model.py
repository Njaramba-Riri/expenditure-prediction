import logging

import yaml

from typing import Tuple
from typing_extensions import Annotated

import numpy as np

from sklearn.base import RegressorMixin
from catboost.core import CatBoostRegressor

from zenml import step
from zenml.client import Client
import mlflow

from utils.regressor.model_train import Linear, RandomForest, CatBoost, XGBoost, Light


experiment_tracker = Client().active_stack.experiment_tracker

with open("src/zenml/steps/regressor/models.yml", "r") as f:
    model_configs = yaml.safe_load(f)

@step(name="Regressor Model Training", enable_cache=True, experiment_tracker=experiment_tracker.name)
def train_regressor(
    X_train: np.ndarray, y_train: np.ndarray) -> Tuple[
        Annotated[CatBoostRegressor, "Catboost Regressor"],
        Annotated[RegressorMixin, "XGB Regressor"],
        Annotated[RegressorMixin, "LGBM Regressor"]
    ]:
    """Pipeline step responsible for training the regressor models.
    
    Args:
        X_train(np.ndarray): Input numpy arrays training features.
        y_train(np.ndarray): Input numpy arrays training target variable.
    
    Returns:
        Regressor trained models.
    
    Raise:
        Exception.
    """
    try:
        model = None
        for model_config in model_configs["models"]:
            model_name = model_config["name"]
            model_parameters = model_config["parameters"]

            # if model_name == "Linear":
            #     model = Linear()
            #     mlflow.sklearn.autolog()
            #     trained_lr = model.train(X_train, y_train, **model_parameters)
            # elif model_name == "Forest":
            #     model = RandomForest()
            #     mlflow.autolog()
            #     trained_rf = model.train(X_train, y_train, **model_parameters)
            if model_name == "CatBoost":
                model = CatBoost()
                #mlflow.catboost.log_model(model,"catboost")
                trained_cat = model.train(X_train, y_train, **model_parameters)
            elif model_name == "XGBoost":
                model = XGBoost()
                mlflow.xgboost.autolog()
                trained_xgb = model.train(X_train, y_train, **model_parameters)
            elif model_name == "LightGBM":
                model = Light()
                mlflow.lightgbm.autolog()
                trained_lgb = model.train(X_train, y_train, **model_parameters)
            else:
                raise ValueError("Model with the name `{}` is not supported.".format(model_name))
        return(trained_cat, trained_xgb, trained_lgb)
    except Exception as e:
        logging.error("Error while training regressor models: {}".format(e))
        raise e