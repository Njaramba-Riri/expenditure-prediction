import logging

import numpy as np

from typing import Tuple, Union
from typing_extensions import Annotated

from sklearn.base import ClassifierMixin
from catboost.core import CatBoostClassifier

from zenml import step
from zenml.client import Client
import mlflow

from utils.classifier.model_eval import PrecisionScore, RecallScore, F1_Score, ROCAUC

experiment_tracker = Client().active_stack.experiment_tracker

@step(enable_cache=False, experiment_tracker=experiment_tracker.name)
def model_evaluate(
    model: Union[ClassifierMixin, CatBoostClassifier],
    X_test: np.ndarray,
    y_test: np.ndarray
) -> Tuple[
    Annotated[float, "precision score"],
    Annotated[float, "recall score"],
    Annotated[float, "f1_score"],
    Annotated[float, "roc_auc score"]
]:
    """Evaluates the trained model using various performance metrics.

    Args:
        model: A trained model object that implements the `ClassifierMixin` interface or is an instance of `CatBoostClassifier`.
        X_test: A numpy array containing the test features.
        y_test: A numpy array containing the test labels.

    Returns:
        A tuple of annotated scores for precision, recall, F1 score, and ROC AUC score.
    """
    try:
        y_true = model.predict(X_test)
        precision = PrecisionScore()
        pre_score = precision.calculate_scores(y_test, y_true)  
        mlflow.log_metric("precision", pre_score)

        rec = RecallScore()
        rec_score = rec.calculate_scores(y_test, y_true)
        mlflow.log_metric("recall", rec_score)

        f1_eval = F1_Score()
        f1 = f1_eval.calculate_scores(y_test, y_true)
        mlflow.log_metric("f1_score", f1)

        roc = ROCAUC()
        predict_proba = model.predict_proba(X_test)
        roc_auc = roc.calculate_scores(y_test, predict_proba)
        mlflow.log_metric("roc_auc", roc_auc)

        return (pre_score, rec_score, f1, roc_auc)
    except Exception as e:
        logging.error("Error while evaluating model: {}".format(e))
        raise e