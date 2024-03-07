import os
import warnings
warnings.filterwarnings("ignore")

import pickle

import numpy as np
from sklearn.preprocessing import LabelEncoder
from .vectorizer import vect

dire = os.path.dirname(__file__)
classifier = pickle.load(open(os.path.join(dire, 'mainapp/pickled', 'Cat_v3.pkl'), 'rb'))
regressor = pickle.load(open(os.path.join(dire, 'mainapp/pickled', 'catregress.pkl'), 'rb'))
clf = pickle.load(open(os.path.join(dire, 'admin/pickle_objects', 'classifier.pkl'), 'rb'))


def staycation(stay_duration):
    if stay_duration <= 7:
        return "week"
    elif stay_duration > 7 <= 14:
        return "2 weeks"
    elif stay_duration > 14 <= 21:
        return "3 weeks"
    elif stay_duration > 21 <= 28:
        return "month"
    elif stay_duration > 28:
        return "eternity"

def predict_category(inputs):
    categories = ['High Cost', 'Higher Cost', 'Highest Cost', 
                'Low Cost', 'Lower Cost', 'Normal Cost']
    le = LabelEncoder()
    le.fit_transform(categories)

    category = classifier.predict(inputs)[0]
    probability = np.max(classifier.predict_proba(inputs)).round(4) * 100 #, le.classes_)))[::-1]
    # probability = classifier.predict_proba(inputs)

    return category, probability

def predict_cost(inputs):
    cost = regressor.predict(inputs)
    predicted_cost = np.exp(cost)
    
    return predicted_cost


def predict_feed_sentiment(feedback):
    labels = { 0: 'Negative', 1: 'Positive'}
    X = vect.transform([feedback])
    y = clf.predict(X)[0]
    probability = np.max(clf.predict_proba(X)).round(4) * 100

    return labels[y], probability
