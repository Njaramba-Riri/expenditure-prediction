import os
import pickle

import pandas as pd

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


dire = os.path.dirname(__file__)
model = pickle.load(open(os.path.join(dire, "../admin/pickle_objects", "Cat_v3.pkl"), 'rb'))

data = pd.read_csv("/home/riri/Desktop/expenditure/src/models/notebooks/classification/Version_1.csv")

for col in data.select_dtypes(['object', 'category']):
    data[col] = data[col].fillna(str("None"))

X = data.drop(columns=['cost_category', 'night_mainland', 'night_zanzibar'], axis=1)
y = data['cost_category']

def get_model_score():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True, random_state=123)
    
    y_pred = model.predict_proba(X_test)
    
    score = roc_auc_score(y_test, y_pred, multi_class='ovr')
    
    return score
