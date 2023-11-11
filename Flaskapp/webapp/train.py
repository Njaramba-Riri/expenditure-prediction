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

train_data = pd.read_csv("../Datasets/Train.csv")
test_data = pd.read_csv("../Datasets/test.csv")

from .predict import model


def train(features, y):
    
    model.partial_fit(features, [y])