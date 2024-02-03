import logging

from typing import Tuple
from typing_extensions import Annotated

import numpy as np
import pandas as pd

from zenml import step 
from zenml.client import Client

from utils.classifier.data_cleaning import DataCleaning, DataPreprocessStrategy, DataSplitStrategy

experiment_tracker = Client().active_stack.experiment_tracker

@step(enable_cache=True, experiment_tracker=experiment_tracker.name)
def data_cleaning(df: pd.DataFrame) -> Tuple[
    Annotated[np.ndarray, "X_train"],
    Annotated[np.ndarray, "X_test"],
    Annotated[np.ndarray, "y_train"],
    Annotated[np.ndarray, "y_test"]
]:
    """Step to clean data and split it into training and testing sets.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be cleaned.
        
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: A tuple of annotated numpy arrays, where
            X_train and X_test are the input features and y_train and y_test are the corresponding labels.
    """
    try:
        logging.info("Preprocessing data with shape: {}".format(df.shape))
        processing_strategy = DataPreprocessStrategy()
        data_preprocess = DataCleaning(df, strategy=processing_strategy)
        cleaned_df = data_preprocess.handle_data()
        logging.info("Done preprocessing all data!: {}".format(cleaned_df.shape[0]))
        logging.info("Starting splitting of the preprocessed data.")
        splitting_strategy = DataSplitStrategy()
        data_split = DataCleaning(cleaned_df, strategy=splitting_strategy)
        X_train, X_test, y_train, y_test = data_split.handle_data()
        logging.info(f"Done splitting data into `X_train`: {X_train.shape}, `X_test`: {X_test.shape}, `y_train`: {y_train.shape}, and `y_test`: {y_test.shape}")
        return (X_train, X_test, y_train, y_test)
    except Exception as e:
        logging.error("Error while cleaning the data: {}".format(e))
        raise e
