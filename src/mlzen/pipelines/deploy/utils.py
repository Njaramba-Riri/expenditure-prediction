import logging

import pandas as pd

from utils.classifier.data_cleaning import DataCleaning, DataPreprocessStrategy

def get_data_for_test():
    try:
        data = pd.read_csv("Datasets/Test.csv")
        data = data.sample(n=100)
        preprocess_strategy = DataPreprocessStrategy()
        data_cleaning = DataCleaning(data, preprocess_strategy)
        data = data_cleaning.handle_data()
        result = data.to_json(orient="split")
        return result
    except Exception as e:
        logging.exception("Couldn't get data for testing: {}".format(e))
        raise e
