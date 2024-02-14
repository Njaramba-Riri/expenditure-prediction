import logging 

from abc import ABC, abstractmethod

import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

class TrainRegressor(ABC):
    """Abstract class that defines the strategy for training regressor models.

    Args:
        ABC (_type_): 
    """
    @abstractmethod
    def train(self, X_train: np.ndarray, y_train: np.ndarray, **kwargs):
        """Attribute that trains the model.

        Args:
            X_train (np.ndarray): Input features in form of numpy arrays.
            y_train (np.ndarray): Input target value
        """
        pass

class Linear(TrainRegressor):
    """Defines the strategy for training the logistic regression model.
    Args:
        TrainRegressor (_type_): Base class.
    """
    def train(self, X_train: np.ndarray, y_train: np.ndarray, **kwargs):
        """Trains linear regression model.

        Args:
            X_train (np.ndarray): Input numpy array features.
            y_train (np.ndarray): Input numpy array target variable.
        Returns:
            Logistic regression classifier.
        Raises:
            Exception
        """
        try:
            lr = LinearRegression(**kwargs)
            trained_lr = lr.fit(X_train, y_train)
            return trained_lr
        except Exception as e:
            logging.error("Error while training logistic regression model: {}".format(e))
            raise e

class RandomForest(TrainRegressor):
    """Class that defines the training of a Random Forest Regressor model.

    Args:
        TrainRegressor (_type_): _description_
    """
    def train(self, X_train: np.ndarray, y_train: np.ndarray, **kwargs):
        """Trains random forest regressor model.

        Args:
            X_train (np.ndarray): Input numpy array features.
            y_train (np.ndarray): Input numpy array target variable.
        Returns:
            Trained random forest classifier.
        Raises:
            Exception
        """
        try:
            rf = RandomForestRegressor(**kwargs)
            trained_rf = rf.fit(X_train, y_train)
            return trained_rf
        except Exception as e:
            logging.info("Error while training random forest regessor model: {}".format(e))
            raise e        
        
class CatBoost(TrainRegressor):
    """Defines the training strategy for the catboost regressor model.

    Args:
        TrainRegressor (_type_): Base inherited class.
    """
    def train(self, X_train: np.ndarray, y_train: np.ndarray, **kwargs):
        """Trains catboost regressor model.

        Args:
            X_train (np.ndarray): Input numpy array features.
            y_train (np.ndarray): Input numpy array target variable.

        Returns:
            CatBoost Regressor: Trained catboost regressor model.

        Raises:
            Exception.  
        """
        try:
            cat = CatBoostRegressor(**kwargs)
            trained_cat = cat.fit(X_train, y_train)
            return trained_cat
        except Exception as e:
            logging.error("Error while training catboost regressor model: {}".format(e))
            raise e

class XGBoost(TrainRegressor):
    """Defines strategy for training xgb regressor model.
    Args:
        TrainRegressor (_type_): Base class.
    """
    def train(self, X_train: np.ndarray, y_train: np.ndarray, **kwargs):
        """Trains XGBoost regressor moderl.

        Args:
            X_train (np.ndarray): Input numpy arrays features.
            y_train (np.ndarray): Input numpy array target variable.

        Returns:
            Regressor: Trained regressor model.
        
        Raises:
            Exception.
        """
        try:
            xgb = XGBRegressor(**kwargs)
            trained_xgb = xgb.fit(X_train, y_train)
            return trained_xgb
        except Exception as e:
            logging.error("Error while training xgboost regressor model: {}".format(e))
            raise e
        
class Light(TrainRegressor):
    """Defines strategy for training regressor.

    Args:
        TrainRegressor (_type_): Base classs.
    """
    def train(self, X_train: np.ndarray, y_train: np.ndarray, **kwargs):
        """Trains LightGBM regressor model.

        Args:
            X_train (np.ndarray): Input numpy array features.
            y_train (np.ndarray): Input numpy array target variable.

        Returns:
            Regressor: Trained LGBMRegressor model.
        
        Raises:
            Exeception.
        """
        try:
            lgb = LGBMRegressor(**kwargs)
            trained_lgb = lgb.fit(X_train, y_train)
            return trained_lgb
        except Exception as e:
            logging.error("Error while training LightGBM regressor model: {}".format(e))
            raise e