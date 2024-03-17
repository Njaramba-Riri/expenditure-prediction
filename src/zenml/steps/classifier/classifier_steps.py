import logging
from typing import Tuple, Union
from typing_extensions import Annotated

import pandas as pd
import numpy as np
from zenml import step
from zenml.client import Client
import mlflow

from utils.classifier.data_cleaning import DataCleaning, DataPreprocessStrategy, DataSplitStrategy
from utils.classifier.model_train import RandomForestClassifier, CatBoost, XGBoost, LightGClassifier
from utils.classifier.model_eval import PrecisionScore, RecallScore, F1_Score, AccuracyScore, ROCAUC

from sklearn.base import ClassifierMixin
from catboost.core import CatBoostClassifier

experiment_tracker = Client().active_stack.experiment_tracker

class LoadData:
    """
    Loading data from the path.
    """
    def __init__(self, data_path: str):
        """
        Initializes the LoadData
        Args:
            data_path (str): path to the data
        """
        self.data_path = data_path

    def get_data(self):
        """
        Loads the data from the path.

        Returns:
            _type_: Pandas Dataframe
        """
        logging.info(f"Loading data from {self.data_path}")
        return pd.read_csv(self.data_path)

@step
def load_data(data_path: str) -> pd.DataFrame :
    """
    Loads the data from data_path

    Args:
        data_path (str): path to the data
    Returns:
        pd.DataFrame: the loaded data
    """
    try:
        load_data = LoadData(data_path)
        df = LoadData.get_data(load_data)
        return df
    except Exception as e:
        logging.error(f"Error when loading the data: {e}")
        raise e
    
@step
def clean_data(df: pd.DataFrame) -> Tuple[
    Annotated[np.ndarray, "X_train"],
    Annotated[np.ndarray, "X_test"],
    Annotated[np.ndarray, "y_train"],
    Annotated[np.ndarray, "y_test"]
] :
    """
    Cleans the loaded dataframe.

    Args:
        df (pd.DataFrame): The dataframe to be cleaned, raw data.

    Returns:
        X_train: Training data
        X_test: Testing data
        y_train: Trainig target variable
        y_test: Testing target variable
    """
    try:
        processing_strategy = DataPreprocessStrategy()
        data_preprocess = DataCleaning(df, strategy=processing_strategy)
        processed_data = data_preprocess.handle_data()

        splitting_strategy = DataSplitStrategy()
        data_cleaning = DataCleaning(processed_data, strategy=splitting_strategy)
        X_train, X_test, y_train, y_test = data_cleaning.handle_data()
        logging.info("Data cleaning completed.")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error("Error while cleaning the data: {}".format(e))
        raise e

@step(experiment_tracker=experiment_tracker.name)
def train_model(
    X_train: Union[np.ndarray, pd.DataFrame], 
    y_train: Union[np.ndarray, pd.DataFrame],
    config: str
    ) -> Union [ClassifierMixin, CatBoostClassifier]:
    """Trains the ML models.

    Args:
        X_train (np.ndarray): Numpy array or pandas dataframe input features.
        y_train (np.ndarray): NUmpy array or pandas dataframe input target feature.
        config (str): Yaml file containing the defined ML algorithms.

    Raises:
        ValueError: _description_
        e: _description_

    Returns:
        Union [ClassifierMixin, CatBoostClassifier]: Base Sklearn classifier mixin or catboost classifier.
    """
    try:
        model = None
        if config.model_name == "XGBoostClassifier":
            model = XGBoost()
            mlflow.xgboost.autolog()
            trained_xgb = model.fit(X_train, y_train)
            return trained_xgb
        elif config.model_name == "RandomForestClassifier":
            model = RandomForestClassifier()
            mlflow.sklearn.autolog()
            trained_forest = model.fit(X_train, y_train)
            return trained_forest
        elif config.model_name == "LGBClassifier":
            model = LightGClassifier()
            mlflow.lightgbm.autolog()
            trained_lgb = model.fit(X_train, y_train)
            return trained_lgb
        elif config.model_name == "CatBoostClassifier":
            model = CatBoost()
            trained_cat = model.train(X_train, y_train)
            return trained_cat
        else:
            raise ValueError("Model {} not supported".format(config.model_name))
    except Exception as e:
        logging.error("Error while trying to train the model: {}".format(e))
        raise e
    
@step(experiment_tracker=experiment_tracker.name)
def evaluate_model(
    model: Union[ClassifierMixin, CatBoostClassifier],
    X_test: np.ndarray, 
    y_test: np.ndarray) -> Tuple[
        Annotated[float, "pre_score"],
        Annotated[float, "rec_score"],
        Annotated[float, "f1"],
        Annotated[float, "roc_auc"],
        Annotated[float, "acc_score"]
    ]:
    try:
        prediction = model.predict(X_test)
        precision = PrecisionScore()
        pre_score = precision.calculate_scores(y_test, prediction)  
        mlflow.log_metric("precision", pre_score)

        rec = RecallScore()
        rec_score = rec.calculate_scores(y_test, prediction)
        mlflow.log_metric("recall", rec_score)

        f1_eval = F1_Score()
        f1 = f1_eval.calculate_scores(y_test, prediction)
        mlflow.log_metric("f1_score", f1)

        roc = ROCAUC()
        predict_proba = model.predict_proba(X_test)
        roc_auc = roc.calculate_scores(y_test, predict_proba)
        mlflow.log_metric("roc_auc", roc_auc)

        acc = AccuracyScore()
        acc_score= acc.calculate_scores(y_test, prediction)
        mlflow.log_metric("Confusion matrix", acc_score)

        return pre_score, rec_score, f1, roc_auc, acc_score
    except Exception as e:
        logging.error("Error while evaluating model: {}".format(e))
        raise e
