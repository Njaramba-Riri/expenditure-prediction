import os
import warnings
warnings.filterwarnings("ignore")

import pickle

import numpy as np
from sklearn.preprocessing import LabelEncoder
from .vectorizer import vect

dire = os.path.dirname(__file__)
model = pickle.load(open(os.path.join(dire, 'pickle_objects', 'cat.pkl'), 'rb'))
clf = pickle.load(open(os.path.join(dire, 'pickle_objects', 'classifier.pkl'), 'rb'))

def predict_details(details):
    y_vals = ['High Cost', 'Higher Cost', 'Highest Cost', 
                'Low Cost', 'Lower Cost', 'Normal Cost']
    le =LabelEncoder()
    le.fit_transform(y_vals)

    y = le.classes_[model.predict(details)[0]]
    proba = np.max(model.predict_proba(details)).round(4)*100#, le.classes_)))[::-1]

    return y, proba

def predict_feed_sentiment(feed):
    labels = { 0: 'Negative', 1: 'Positive'}
    X = vect.transform([feed])
    y = clf.predict(X)[0]
    probability = np.max(clf.predict_proba(X)).round(4) * 100

    return labels[y], probability