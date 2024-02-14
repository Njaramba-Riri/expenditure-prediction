import logging

from abc import ABC, abstractmethod

from typing import Union

import pandas as pd
import numpy as np
from pandas.core.api import Series as Series

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, RobustScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, StratifiedKFold

class DataStrategy(ABC):
    """Abstract class defining the blueprint of handling data.

    Args:
        ABC (_type_): Helper class for creating ABC using inheritance.
    """
    @abstractmethod
    def clean_data(self, df: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        """Attribute of the DataStrategy class that when call, it handles the specific function of cleaning data.

        Args:
            df (pd.DataFrame): Input pandas dataframe.

        Returns:
            Union[pd.DataFrame, pd.Series]: A pandas dataframe or series.
        """
        pass


class DataCleanStrategy(DataStrategy):
    """Defines the strategy for cleaning the data.

    Args:
        DataStrategy (_type_): Abstract inherited class
    """
    def clean_data(self, df: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        """Handles the cleaning of the dataframe.

        Args:
            df (pd.DataFrame): The input dataframe containing both numerical and categorical columns.

        Returns:
            Union[pd.DataFrame, pd.Series]: The output pandas dataframe or series.
        """
        try:
            df.drop_duplicates(keep='first', inplace=True)
            return df
        except Exception as e:
            logging.error("Error while cleaning dataframe: {}".format(e))
            raise e

class DataPreprocessStrategy(DataStrategy):
    """Defines the strategy for preprocesing of the data.

    Args:
        DataStrategy (_type_): Abstract inherited ABC class.
    """
    def clean_data(self, df: pd.DataFrame) -> np.ndarray:
        """Handles the preprocessing of the data.

        Args:
            df (pd.DataFrame): Input pandas dataframe. 

        Returns:
            Union[pd.DataFrame, pd.Series, np.ndarray]: Numpy arrays of preprocessed data.
        """
        try:
            df.drop('total_cost', axis=1, inplace=True)
            numerical = df.select_dtypes(include=np.number).columns.to_list()
            categorical = df.select_dtypes(exclude=np.number).columns.to_list()

            for col in categorical:
                num_unique = df[col].nunique()
                if num_unique <= 5:
                    categorical_pipe = make_pipeline(SimpleImputer(strategy='constant', fill_value=str('None')),
                                                     OrdinalEncoder())
                else:
                    categorical_pipe = make_pipeline(SimpleImputer(strategy='constant', fill_value=str('None')),
                                                     OneHotEncoder(sparse_output=False, max_categories=30))
            
            numerical_pipeline = make_pipeline((SimpleImputer(strategy="median")),
                                               ('scaler', RobustScaler()))

            transformer = ColumnTransformer(transformers=[
                ("numerical", numerical_pipeline, numerical),
                ("categorical", categorical_pipe, categorical)
            ])

            pipeline = Pipeline(steps=[
                ('transformer', transformer),
                ('scaler', StandardScaler())
            ])

            inputs = pipeline.fit_transform(df)
            target = np.array(df['total_cost'])
            X_train, X_test, y_train, y_test = train_test_split(inputs, target, test_size=0.2,
                                                                shuffle=True, random_state=42)
            
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logging.error("Error while preprocessing the dataframe: {}".format(e))
            raise e
        
# class DataSplitStrategy(DataStrategy):
#     """Defines the strategy to split data ready for model training and evaluation.

#     Args:
#         DataStrategy (_type_): Abstract inheritance class.
#     """
#     def clean_data(self, X: np.ndarray, y: Union[np.ndarray, pd.Series, pd.DataFrame]) -> np.ndarray:
#         """Splits the input variables as well as the target variable.

#         Args:
#             X (np.ndarray): Input features.
#             y (Union[np.ndarray, pd.Series, pd.DataFrame]): Target feature.

#         Returns:
#             np.ndarray: Numpy array of split features.
#         """
#         try:
#             n_folds = 10
#             k_folds = StratifiedKFold(n_folds, shuffle=True, random_state=42)

#             for(train_idx, val_idx) in k_folds.split(X, y):
#                 X_train, X_test = X[train_idx], X[val_idx]
#                 y_train, y_test = y[train_idx], y[val_idx]

#             return X_train, X_test, y_train, y_test
#         except Exception as e:
#             logging.error("Error while splitting the data: {}".format(e))
#             raise e
        
class DataCleaning:
    """Cleans and preprocesses data using a specified data strategy.

    Args:
        df (pd.DataFrame): The input data as a pandas DataFrame.
        strategy (DataStrategy): The data strategy used for cleaning and preprocessing.

    Attributes:
        df (pd.DataFrame): The input data as a pandas DataFrame.
        strategy (DataStrategy): The data strategy used for cleaning and preprocessing.
    """

    def __init__(self, df: pd.DataFrame, strategy: DataStrategy):
        self.df = df
        self.strategy = strategy

    def clean_data(self) -> np.ndarray:
        """Cleans and preprocesses the data using the specified data strategy.

        Returns:
            np.ndarray: The cleaned and preprocessed data.
        """
        try:
            return self.strategy.clean_data(self.df)
        except Exception as e:
            logging.error(f"Error while cleaning and preprocessing the data: {e}")
            raise e