import logging
from abc import ABC, abstractmethod

import numpy as np

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score,  \
    precision_score, recall_score, accuracy_score

class ModelEval(ABC):
    """Abstract class defining strategy for evaluating classifier models.
    """
    @abstractmethod
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """Calculates the scores of the model.

        Args:
            y_true (np.ndarray): True labels.
            y_pred (np.ndarray): Predicted labels.
        """
        pass
class PrecisionScore(ModelEval):
    """Calculates the precision score of the model.
    """
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        try: 
            logging.info("Calculating precision score...")
            pre = precision_score(y_true, y_pred, average="weighted")
            logging.info("Precision Score: {}".format(pre))
            return pre
        except Exception as e:
            logging.error("Error while trying to calculate precision score: {}".format(e))
            raise e

class RecallScore(ModelEval):
    """Calculates the recall score of the model.
    """
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        try: 
            logging.info("Calculating recall score...")
            rec = recall_score(y_true, y_pred, average="weighted")
            logging.info("Precision Score: {}".format(rec))
            return rec
        except Exception as e:
            logging.error("Error while trying to calculate precision score: {}".format(e))
            raise e

class F1_Score(ModelEval):
    """Calculates the F1 score of the models.
    """    
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculates the F1 score of the model

        Args:
            y_true (np.ndarray): Array of true labesl.
            y_pred (np.ndarray): Array of predicted labesl.

        Raises:
            e: If there's an error while calculating the scores.

        Returns:
            float: F1 Score
        """
        try:
            logging.info("Calculating F1 Score...")
            f1 = f1_score(y_true, y_pred, average="weighted")
            logging.info("F1 Score: {}".format(f1))
            return f1
        except Exception as e:
            logging.error("Error while calculating the f1 score: {}".format(e))
            raise e
        
class AccuracyScore(ModelEval):
    """Calculates the confusion matrix of the model.
    """
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        try: 
            logging.info("Calculating accuracy score...")
            acc = accuracy_score(y_true, y_pred)
            logging.info("Accuracy score: {}".format(acc))
            return acc
        except Exception as e:
            logging.error("Error while trying to calculate accuracy score: {}".format(e))
            raise e
        
class ROCAUC(ModelEval):
    """Calculates the ROC AUC score of the models.
    """
    def calculate_scores(self, y_true: np.ndarray, y_score: np.ndarray) -> float:
        """Calculates the ROC AUC score of the model.

        Args:
            y_true: Array of true labels.
            y_score: Array of predicted scores.

        Returns:
            The ROC AUC score.

        Raises:
            Exception: If there is an error while calculating the ROC AUC score.
        """
        try:
            logging.info("Calculating ROC AUC score...")
            roc = roc_auc_score(y_true, y_score, average="weighted", multi_class="ovr")
            logging.info("ROC AUC Score: {}".format(roc))
            return roc
        except Exception as e:
            logging.error("Error while trying to calculate ROC AUC score: {}".format(e))
            raise e