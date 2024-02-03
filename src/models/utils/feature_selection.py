from rich import print

import pandas as pd

from sklearn.feature_selection import RFE, SelectFromModel
from sklearn.ensemble import RandomForestRegressor

from .load import load_data
from .preprocessing import clean_data
from .transformers import transform_data

train = load_data("Train (1).csv")
#train.drop('ID', axis=1, inplace=True)
train = clean_data(train)

#X = train.drop('total_cost', axis=1)
X, y = transform_data(train)
#y = train['total_cost']

model = RandomForestRegressor()

sfm = SelectFromModel(model, max_features=15)
transformed = sfm.fit_transform(X, y)

support = sfm.get_support()



print([
    x for x in support
])