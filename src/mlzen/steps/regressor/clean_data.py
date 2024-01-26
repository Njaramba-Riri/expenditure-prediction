import logging

from typing import Tuple
from typing_extensions import Annotated

import pandas as pd
import numpy as np

from zenml import step
from zenml.client import Client

from utils.regressor.data_cleaning import DataCleanStrategy, DataPreprocessStrategy, \
    DataSplitStrategy, DataCleaning

experiment_tracker = Client().active_stack.experiment_tracker

@step(name="Data Cleaning", enable_cache=True, experiment_tracker=experiment_tracker.name)
def data_clean(df: pd.DataFrame) -> Tuple[
    Annotated[np.ndarray, "X_train"],
    Annotated[np.ndarray, "X_test"],
    Annotated[np.ndarray, "y_train"],
    Annotated[np.ndarray, "y_test"]
]:
    """Cleans the dataframe by handling the missing values, and more.

    Args:
        df: The loaded dataframe from the load data step.
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: A tuple of annotated numpy arrays whereby X_train \
        and X_test are the input variables whereas y_train and y_test are their corresponding ground values.
    """     
    try:
        logging.info("Cleaning data with shape: {}".format(df.shape))
        clean_strategy = DataCleanStrategy()
        data_clean = DataCleaning(df, strategy=clean_strategy)
        cleaned_df = data_clean.clean_data()
        logging.info("Done cleaning all data: {}".format(cleaned_df.shape))
        logging.info("Preprocessing cleaned dataframe...")
        preprocess_strategy = DataPreprocessStrategy()
        data_prepro = DataCleaning(cleaned_df, strategy=preprocess_strategy)
        preprocessed = data_prepro.clean_data()
        logging.info("Preprocessing of the dataframe is complete, shape: {}".format(preprocessed.shape[0]))
        logging.info("Splitting of the preprocessed data...")
        split_strategy = DataSplitStrategy()
        data_split = DataCleaning(preprocessed, strategy=split_strategy)
        X_train, X_test, y_train, y_test = data_split.clean_data()
        logging.info(f"Done splitting data into `X_train`:{X_train.shape}, `X_test`:{X_test.shape}, `y_train`:{y_train.shape}, `y_test`:{y_test.shape}")
        return (X_train, X_test, y_train, y_test)
    except Exception as e:
        logging.exception("Error while cleaning the loaded dataframe: {}".format(e))
        raise e


