import numpy as np

from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from webapp import db

def transform(user_input):
    data = np.array(user_input)

    for country in data:
        region = db.query.filter_by(country)
        