import logging 
from abc import ABC, abstractmethod

from sklearn.ensemble import RandomForestClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

class Model(ABC):
    """
    Abstract class for all the models.

    Args:
        ABC (_type_): _description_
    """
    @abstractmethod
    def train(X_train, y_train):
        """
        Trains the model.

        Args:
            X_train (_type_): Training features
            y_train (_type_): Training labels
        """
        pass

class RandomForest(Model):
    """
    Random forest classifier.

    Args:
        Model (_type_): _description_
    """
    def train(self, X_train, y_train, **kwargs):
        """
        Trains the model

        Args:
            X_train (_type_): Training variables.
            y_train (_type_): Target variable.
        """
        try:
            forest = RandomForestClassifier(**kwargs)
            logging.info("Training RandomForestClassifier...")
            forest.fit(X_train, y_train)
            logging.info("Training RandomForestClassifier completed.")
            return forest
        except Exception as e:
            logging.error("Error while training forest classifier: {}".format(e))
            raise e


class CatBoost(Model):
    """
    Trains a catboost classifier.

    Args:
        Model (_type_): Base model class.
    """
    def train(self, X_train, y_train, **kwargs):
        """
        Trains the model.

        Args:
            X_train (_type_): Training variables
            y_train (_type_): Training target variable.
        """
        try:
            cat = CatBoostClassifier(**kwargs)
            logging.info("Training catboost classifier...")
            cat.fit(X_train, y_train)
            logging.info("Done training catboost classifier.")
            return cat
        except Exception as e:
            logging.error("Error while training catboost classifier: {}".format(e))
            raise e

class XGBoost(Model):
    """
    Trains an xgboost classifier.

    Args:
        Model (_type_): Base model class.
    """
    def train(self, X_train, y_train, **kwargs):
        """
        When called, trains the XGBClassifier model.

        Args:
            X_train (_type_): Input np.ndarray features
            y_train (_type_): Target np.ndarray feature.
        """
        try:
            xgb = XGBClassifier(**kwargs)
            logging.info("Training XGBoost classifier...")
            xgb.fit(X_train, y_train)
            logging.info("Training XGBClassifier is completed.")
            return xgb
        except Exception as e:
            logging.error("Errro while training XGBoost classifier: {}".format(e))
            raise e

class LightGClassifier(Model):
    """
    Trains lightgbm classifier.

    Args:
        Model (_type_): Base model class.
    """
    def train(self, X_train, y_train, **kwargs):
        """
        When called, trains the LGBClassifier model.

        Args:
            X_train (_type_): Input np.ndarray features.
            y_train (_type_): Training np.ndarray target feature.
        """
        try:
            lgb = LGBMClassifier(**kwargs)
            logging.info("Training LGBClassifier model...")
            lgb.fit(X_train, y_train)
            logging.info("Training LGBClassifier is completed.")
            return lgb
        except Exception as e:
            logging.error("Error while training LGBClassifier: {}".format(e))
            raise e
        