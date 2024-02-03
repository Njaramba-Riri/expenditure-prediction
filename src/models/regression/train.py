import os
import pickle

from rich import print

from typing import Union, Tuple, Annotated

import numpy as np

from sklearn.base import RegressorMixin
from catboost.core import CatBoostRegressor

from sklearn.metrics import mean_squared_error, r2_score

def train_regressor(Regressor: Union[RegressorMixin,
                                      CatBoostRegressor],
                    X_train: np.ndarray, 
                    y_train: np.ndarray, **kwargs) -> Union[RegressorMixin, 
                                                            CatBoostRegressor]:
        """Trains the regressor models.

        Args:
            Regressor (Union[RegressorMixin, CatBoostRegressor]): THe regressor to be used, can either inherit from sklearn 
                            regressor base class or a catboost.
            X_train (np.ndarray): Input training feaures as numpy arrays.
            y_train (np.ndarray): Input target variable as a numpy array.

        Returns:
            Union[RegressorMixin, CatBoostRegressor]: Trained regressor model.
        """
        regressor = Regressor(**kwargs)

        regressor.fit(X_train, y_train)
        
        return regressor


def evaluate_model(Regressor: Union[RegressorMixin, CatBoostRegressor], 
                   X_test: np.ndarray, y_test: np.ndarray) -> Tuple[float, float, float]:
    """Evaluates the regressor model.

    Args:
        Regressor (Union[RegressorMixin, CatBoostRegressor]): Regressor model to be evaluated, have to implement sklearn regressor mixin or catboost.
        X_test (np.ndarray): Input evaluation features as numpy arrays.
        y_test (np.ndarray): Input evaluation target label as a numpy array.

    Returns:
        Tuple[float, float, float]: Flaot values of MSE, RMSE, R2 Score.
    """

    y_pred = Regressor.predict(X_test)

    mse = mean_squared_error(y_true=y_test, y_pred=y_pred)    
    rmse = np.sqrt(mse)
    R2 = r2_score(y_true=y_test, y_pred=y_pred)

    print(f"\n\nModel: {Regressor}\nMSE: {mse}\nRMSE: {rmse}\nR2: {R2}")

    return mse, rmse, R2
                    
def pickle_regressor(regressor: Union[RegressorMixin, CatBoostRegressor],
                     accuracy: float,  path: str = "pickled_models") -> None:
    """Serializes and stores the model.

    Args:
        regressor (Union[RegressorMixin, CatBoostRegressor]): The trained regressor model to be pickled.
        accuracy (float): Accuracy of the trained regressor model.
        path (str, optional): Destination path where the pickled model will be saved. Defaults to "pickled_models".
    """
    if accuracy >= 0.0:
        if not os.path.exists(path):
            os.makedirs(path)

            filename = os.path.join(path, type(regressor).__name__ + '.pkl')

            with open (filename, 'wb') as f:
                pickle.dump(regressor, f, protocol=pickle.HIGHEST_PROTOCOL)
              
            print(f"Model with accuracy `{accuracy}` saved at `{path}`.")
        else:
             print(f"Model not saved, `{accuracy}` accuracy is below the threshold.")

def unpickle_regressor(path: str) -> Union[RegressorMixin, CatBoostRegressor]:
    """Unserializes the pickled model.

    Args:
        path (str): Path to the pickled model.

    Returns:
        Union[RegressorMixin, CatBoostRegressor]: Either one of either a model that inherits sklearn's regressor base class or a catboost regressor.
    """
    with open(path, 'rb') as f:
        
        regressor = pickle.load(f)

    return regressor