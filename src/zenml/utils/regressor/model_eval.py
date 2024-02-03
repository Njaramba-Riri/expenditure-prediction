import logging

from abc import ABC, abstractmethod

import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

class EvaluateModel(ABC):
    """ Abstract class defininng strategy for calculating regressor model scores.
    """

    @abstractmethod
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        """
        pass

class MSE(EvaluateModel):
    """Calculates the Mean Squared Error of the regressor models.
    """
    def calculate_scores(self, y_true, y_pred, **kwargs):
        """Calcuates the MSE score of the model.

        Args:
            y_test: Actual value of the inputs.
            y_pred: Predicted output value of the input.
        Returns:
            MSE Score. 
        """
        try: 
            logging.info("Calculating MSE...")
            mse = mean_squared_error(y_true, y_pred)
            logging.info("MSE: {:.4f}".format(mse))
            return mse
        except Exception as e:
            logging.error("Error while calsculating MSE: {}".format(e))
            raise e

class RMSE(EvaluateModel):
    """Calculates the Root Mean Squared error of the regressor models. 
    """
    def calculate_scores(self, y_true, y_pred):
        """Calculates the RMSE of the model.

        Args:
            y_true (_type_): Actual values on the ground. (Ground truth).
            y_pred (_type_): Predicted value of the the inputs.
        
        Returns:
            RMSE Score
        """
        try:
            logging.info("Calculating RMSE...")
            rmse = mean_squared_error(y_true, y_pred, squared=False)
            logging.info("RMSE Score: {:.4f}".format(rmse))
            return rmse
        except Exception as e:
            logging.error("Error while calculating RMSE: {}".format(e))
            raise e

class MAE(EvaluateModel):
    """Calculates the Mean Absolute Error of the regressor models.
    """
    def calculate_scores(self, y_true, y_pred):
        """Calculates the MAE of the model.

        Args:
            y_true (_type_): Ground truth/ or actual value of the input.
            y_pred (_type_): Predicted output value of the model.
        
        Returns:
            MAE Score.
        """
        try:
            logging.info("Calculating MAE...")
            mae = mean_absolute_error(y_true, y_pred)
            logging.info("MAE: {:.4f}".format(mae))
            return mae
        except Exception as e:
            logging.error("Error while calculating MAE: {}".format(e))
            raise e

class R2SCORE(EvaluateModel):
    """Calculates the r2 score of regression models.

    Args:
        EvaluateModel (_type_): Base abstract class.
    """
    def calculate_scores(self, y_true, y_pred):
        """Calculates r2 Score

        Args:
            y_true (np.ndarray): Actual value of the inputs. 
            y_pred (_type_): Predicted output value.

        Returns:
            r2 score.
        """
        try:
            logging.info("Calculating R2 Score...")
            r2 = r2_score(y_true, y_pred)
            logging.info("R2 Score: {:.4f}".format(r2))
            return r2
        except Exception as e:
            logging.error("Error while calculating R2 Score: {}".format(e))
            raise e