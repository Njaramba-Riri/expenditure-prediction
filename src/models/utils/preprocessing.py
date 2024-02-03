import warnings
warnings.filterwarnings("ignore")

from rich import print

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from .load import load_data

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Cleans the dataframe by handling missing values and removing outliers.

    Args:
        data (pd.DataFrame): Input dataframe.
    Returns:
        pd.DataFrame: Output dataframe.
    """
    data.drop(['ID'], axis=1, inplace=True)
    numerical = data.select_dtypes(include=np.number)
    categorical = data.select_dtypes(exclude=np.number)

    for col in numerical:
        data[col] = data[col].fillna(int(data[col].median()))

        #Check for the lower, upper quantiles as well as  lower and upper bounds.
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        #Replace outliers with median.
        data.loc[((data[col] < lower_bound) | (data[col] > upper_bound ), col)] = data[col].median()

    for col in  categorical:
        data[col] = data[col].fillna(str("None"))
    
    return data