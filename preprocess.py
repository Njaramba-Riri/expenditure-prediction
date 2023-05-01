import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.impute import ColumnTransformer
from sklearn.pipeline import Pipeline

def preprocessor(X):
    num=col in X.select_dtypes('int','object').columns
    