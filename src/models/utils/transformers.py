from typing import Union, Annotated

import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, RobustScaler, PolynomialFeatures
from sklearn.compose import ColumnTransformer

def transform_data(df: pd.DataFrame) -> Union[np.ndarray, pd.Series, pd.DataFrame]:
    """Transform the dataframe representation.

    Args:
        df (pd.DataFrame): Input dataframe.

    Returns:
        Union[np.ndarray, pd.Series, pd.DataFrame]: An object of either numpy array, pandas series, or a dataframe data type. 
    """
    df = df[:-1]
    target = df['total_cost']
    #df.drop('total_cost', axis=1, inplace=True)

    categorical = []
    nummerical = [c for c in df.select_dtypes('int','float').columns]
    for col in df.select_dtypes(['object', 'category']).columns:
        categorical.append(col)

        numerical_pipeline=Pipeline(steps=[
            ("imputer", SimpleImputer(strategy='median')),
            ("scaler", StandardScaler()),
        ])

        categorical_pipeline=Pipeline(steps=[
            ("imputer", SimpleImputer(strategy='most_frequent')),
            ("encoder", OneHotEncoder(sparse_output=False, max_categories=30)),
            # ("cubic", PolynomialFeatures(degree=1))
        ])

        transformer=ColumnTransformer(transformers=[ 
            ("numerical", numerical_pipeline, nummerical),
            ("categorical", categorical_pipeline, categorical)
        ])
        
        #transformer.set_output(transform="pandas")
        X = transformer.fit_transform(df[nummerical + categorical])
        target = df['total_cost']
        target = np.array(target)
    #print(X.shape, target.shape)
    return X, target



