import logging 

from typing import Tuple, Union
from typing_extensions import Annotated

import numpy as np

from sklearn.base import RegressorMixin
from catboost.core import CatBoostRegressor

from zenml import step
from zenml.client import Client
import mlflow

from utils.regressor.model_eval import MSE, RMSE, MAE, R2SCORE 

experiment_tracker = Client().active_stack.experiment_tracker

@step(name="Model Evaluation", enable_cache=True, experiment_tracker=experiment_tracker.name)
def evaluate_regressor(
    model: Union[RegressorMixin, CatBoostRegressor],
    X_test: np.ndarray, 
    y_test: np.ndarray) -> Tuple[
        Annotated[float, "Mean Squared Error"],
        Annotated[float, "Root Mean Squared Error"],
        Annotated[float, "Mean Absolute Error"],
        Annotated[float, "R2 Score"]
        ]:
    """Pipeline step responsible for evaluating regressor models.

    Args:
        model: A trained model that implements `RegressorMixin` interface or is an instance of `CatBoostRegressor`.
        X_test(np.ndarray): Input numpy arrays validation features.
        y_test(np.ndarray): Input numpy arrays validation target variable.
    
    Returns:
        Tuple[]: Model Scores.
    
    Raises: 
        Exception.
    """
    try:
        y_pred = model.predict(X_test)

        mse = MSE()
        mse_score = mse.calculate_scores(y_test, y_pred)
        mlflow.log_metric("Mean Squared Error", mse_score)

        rmse = RMSE()
        rmse_score = rmse.calculate_scores(y_test, y_pred)
        mlflow.log_metric("Root Mean Squared Error", rmse_score)

        mae = MAE()
        mae_score = mae.calculate_scores(y_test, y_pred)
        mlflow.log_metric("Mean Absolute Error", mae_score)

        r2 = R2SCORE()
        r2_score = r2.calculate_scores(y_test, y_pred)
        mlflow.log_metric("R2 Score", r2_score)

        return (mse_score, rmse_score, mae_score, r2_score)
    except Exception as e:
        logging.error("Error while evaluating the model: {}".format(e))
        raise e

    