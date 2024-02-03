import itertools
from rich import print

import pandas as pd

from .load import load_data
from .preprocessing import clean_data

train = load_data("Train (1).csv")
countries = load_data("all.csv")

def extra_features(df: pd.DataFrame, categorical_cols: list):
    region_df = countries 
    region_df.drop("Alpha")

    combi = list(itertools.combinations(categorical_cols, 2))

    for cat1, cat2 in combi:
        df.loc[:, cat1 + "_" + cat2] = df[cat1].astype(str) + "_" + df[cat2].astype(str)

    
    return df

def handle_numerical(df: pd.DataFrame, numerical_cols: list):
    """Defines strategy for handling numerical data.

    Args:
        df (pd.DataFrame): Input pandas dataframe.
        numerical_col (list): Input numerical columns.
    
    Returns:
        df (pd.DataFrame): A pandas dataframe with new numerical columns.
    """
    for col in numerical_cols:
        df.loc[:, col + '_' + "binned"] = pd.cut(df[col], bins=5, labels=False)
    
    return df 


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Performs feature engineering on input features.

    Args:
        df (pd.DataFrame): Input pandas dataframe on which features will be engenieered.

    Returns:
        pd.DataFrame: Output feature engineered pandas dataframe.
    """
    df['total_people'] = df['total_male'] + df ['total_female']
    aggs = {}

    #Aggregate categoricals with number of unique values and the mean.
    aggs['travel_with'] = ['nunique', 'count']
    aggs['purpose'] = ['nunique', 'count']
    aggs['main_activity'] = ['nunique', 'count']
    
    #For numerical, calculate the sum, mean, max, min of the column.
    aggs['total_people'] = ['sum', 'mean', 'max', 'min']

    agg_df = df.groupby('info_source').agg(aggs)
    agg_df.reset_index(inplace=True)

    return agg_df

if __name__ == "__main__":
    train = load_data("Train (1).csv")
    train = clean_data(train)
    combined = extra_features(train, ['travel_with', 'purpose', 'main_activity'])
    numerical = handle_numerical(train, ['total_male', 'total_female','night_mainland', 'night_zanzibar'])
    #agg_df = engineer_features(train)
    #print(numerical.head())
    #print(numerical.describe())
    for col in combined:
        print(combined[col].value_counts())