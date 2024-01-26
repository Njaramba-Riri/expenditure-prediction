import logging

import pandas as pd
import numpy as np

from zenml import step

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
def data_load(data_path: str) -> pd.DataFrame :
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
    