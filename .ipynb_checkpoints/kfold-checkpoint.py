from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score

from pipelines import preprocessor, preprocessor2
import pandas as pd
import numpy as np    


fold=StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

pipe1=preprocessor()
pipe2=preprocessor2()

models={
    "Tree": DecisionTreeClassifier(),
    "Forest": RandomForestClassifier(),
    "SVM": SVC(),
    "XGBoost": XGBClassifier(),
    "Lgbm": LGBMClassifier(),
    "NNN": MLPClassifier()
}

vectors={
    "Pipe1": pipe1,
    "Pipe2": pipe2
}


def skfold(model, sample, y, kfold):
    
    results={}
    
    results['model_name']=model+"_"+sample
    
    model=model[classification_model]
    X=vectors[sample]
    
    for fold, (train_idx,val_idx) in enumerate(kfold.split(X,y)):
        X_train, X_val= X[train_idx], X[val_idx]
        y_train, y_val=y[train_idx], y[val_idx]
    
        
        model.fit(X_train, y_val)
        y_pred=model.predict(X_val)
        
        
        results["kfold_{}".format(fold+1)]=f1_score(y_val, y_pred)
    return results
    
    
    
    
    