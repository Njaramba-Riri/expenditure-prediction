import os 
import pickle
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import seaborn as sns

from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.pipeline import make_pipeline, Pipeline
from .vectorizer import vect

cur_dir = os.path.dirname(__file__)
clflm = pickle.load(open(os.path.join(cur_dir, 'admin/pickle_objects', 'classifier.pkl'), 'rb'))

train_data = pd.read_csv("~/Desktop/expenditure/Datasets/Train.csv")
test_data = pd.read_csv("~/Desktop/expenditure/Datasets/Test.csv")

from .predict import model


def train_clf(feedback, y):
    X = vect.transform([feedback])
    classifier = clflm.partial_fit(X, [y])

    trained = ""
    #pickle.dump(open(os.path.join(cur_dir, 'pickle_objects', 'updated_clf.pkl'), 'wb'), 
    #                       protocol=pickle.HIGHEST_PROTOCOL)
    
    return trained

def train(features, y):
    model.partial_fit(features, [y])