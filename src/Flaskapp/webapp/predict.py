import os
import warnings
warnings.filterwarnings("ignore")

import pickle

import numpy as np
from sklearn.preprocessing import LabelEncoder
from .vectorizer import vect

dire = os.path.dirname(__file__)
model = pickle.load(open(os.path.join(dire, 'admin/pickle_objects', 'Cat.pkl'), 'rb'))
clf = pickle.load(open(os.path.join(dire, 'admin/pickle_objects', 'classifier.pkl'), 'rb'))

def predict_details(data):
    categories = ['High Cost', 'Higher Cost', 'Highest Cost', 
                'Low Cost', 'Lower Cost', 'Normal Cost']
    le =LabelEncoder()
    le.fit_transform(categories)

    category = le.classes_[model.predict(data)[0]]
    probability = np.max(model.predict_proba(data)).round(4) * 100 #, le.classes_)))[::-1]

    return category, probability

def predict_feed_sentiment(feedback):
    labels = { 0: 'Negative', 1: 'Positive'}
    X = vect.transform([feedback])
    y = clf.predict(X)[0]
    probability = np.max(clf.predict_proba(X)).round(4) * 100

    return labels[y], probability