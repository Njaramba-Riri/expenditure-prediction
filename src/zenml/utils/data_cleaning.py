import logging
from abc import ABC, abstractmethod
from typing import Union

import pandas as pd
from pandas.core.api import DataFrame as DataFrame, Series as Series
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import HashingVectorizer


class DataStrategy(ABC):
    """
    Abstract class defining strategy for handling data.

    Args:
        ABC (_type_): _description_
    """
    @abstractmethod
    def handle_data(self, df: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        pass
        

class DataPreprocessStrategy(DataStrategy):
    """
    Strategy for preprocessing data.

    Args:
        DataStrategy (_type_): Base strategy class.
    """
    def handle_data(self, df: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        """
        Handles preprocessing of columns in the dataframe.

        Args:
            df (DataFrame): The input dataframe containing numerical columns.

        Returns:
            DataFrame | Series: The output dataframe containing processed numerical data.
        """
        try:
            df.drop(['Tour_ID'], axis=1)
            df['country'].replace(
                {
                    'UAE': "UNITED ARAB EMIRATES",
                    'SWIZERLAND': 'SWITZERLAND',
                    'MALT': 'MALTA',
                    'COSTARICA': 'COSTA RICA',
                    'COMORO': 'COMOROS',
                    'SAUD ARABIA': 'SAUDI ARABIA',
                    'PHILIPINES': 'PHILIPPINES',
                    'ECUADO': 'ECUADOR',
                    'UKRAIN':'UKRAINE',
                    'SOMALI':'SOMALIA',
                    'TRINIDAD TOBACCO': 'TRINIDAD AND TOBAGO',
                    'MONECASQUE': 'MOZAMBIQUE',
                    'DJIBOUT': 'DJIBOUTI',
                    'BURGARIA': 'BULGARIA',
                    'United Kingdom of Great Britain and Northern Ireland': 'UNITED KINGDOM'
                }, inplace=True)
            df['age_group'].replace(
                 {
                      '<18':'1-17', 
                      '65+':'65-84'
                }, inplace=True)
            df['total_male'].fillna(df['total_male'].median(), inplace=True)
            df['total_female'].fillna(df['total_female'].median(), inplace=True)
            df['travel_with'].fillna(df['travel_with'].mode(), inplace=True)
            df['main_activity'].replace({"Widlife Tourism": "Wildlife Tourism"}, inplace=True)

            df.drop_duplicates(keep='first', inplace=True)
            return df
        except Exception as e:
            logging.error("Error while processing data: {}".format(e))
            raise e
        
class DataSplitStrategy(DataStrategy):
    """
    Data splitting strategy.
    """

    def handle_data(self, df: pd.DataFrame) -> Union[pd.DataFrame, pd.Series, np.ndarray]:
        """
        Handles splitting of the data into test and train.
        """
        try:                    
            X = df.drop(['cost_category'], axis=1)
            y = df['cost_category']

            numerical_columns = X.select_dtypes(include=np.number).columns.tolist()
            many_cats = []
            normal_cats = []
            for column in X.select_dtypes(exclude=np.number).columns:
                unique_values = len(X[column].unique())
                if unique_values >= 200:
                    many_cats.append(column)
                else:
                    normal_cats.append(column)

            target_column = ['cost_category']
           
           #Pipeline to handle numerical columns.
            numerical_pipeline = Pipeline(steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", RobustScaler())
            ])


            #Pipeline to handle the categorical columns.
            categorical_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy='most_frequent')),
                ("encoder", OneHotEncoder(sparse_output=False, max_categories=60)),
                ("scaler", StandardScaler())
            ])

            # cats = Pipeline(steps=[
            #     ("hasher", HashingVectorizer(n_features=30, alternate_sign=False,
            #                                  norm=None, ngram_range=(1, 1), binary=False))
            # ])

            #Pipeline to handle the target variable.
            target_encoder = LabelEncoder()

            #Combining the pipelines to transform the data.
            transformer = ColumnTransformer(
                transformers=[
                    ("numerical", numerical_pipeline, numerical_columns),
                    ("categorical", categorical_pipeline, normal_cats),
                    # ("huge_categorical", cats, many_cats)
                ]
            )

            features = df[numerical_columns + normal_cats] 
            X = transformer.fit_transform(features)
            y = target_encoder.fit_transform(df[target_column])

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True,  random_state=42)
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logging.error("Error while splitting the data: {}".format(e))
            raise e
        
        
class DataCleaning:
    """
    Cleans the data by processing it and then splitting it into train and test sets.
    """
    def __init__(self, df: pd.DataFrame, strategy: DataStrategy):
        self.df = df
        self.strategy = strategy

    def handle_data(self) -> Union[pd.DataFrame, pd.Series, np.ndarray]:
        """_summary_

        Returns:
            Union[pd.DataFrame, pd.Series]: _description_
        """
        try:
            return self.strategy.handle_data(self.df)
        except Exception as e:
            logging.error("Error while cleaning the data: {}".format(e))
            raise e
        