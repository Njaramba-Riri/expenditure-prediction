import numpy as np

from sklearn.model_selection import GridSearchCV

def model_selection(classifier): 
    gs = GridSearchCV(estimator=classifier,
                 param_grid=[{
                     "n_estimators":[ 200, 300, 400],
                     "max_depth":[3, 4, 5, 6],
                     "criterion":['gini', 'entropy', 'log_loss']
                 }],
                 cv=2, scoring='roc_auc', n_jobs=-1, verbose=1)

    gs.fit(X_train, y_train)
    
    scores = cross_val_score(gs, X_train, y_train,
                       cv=5, scoring='roc_auc')

    print('AUC Score: %.3f (+/- %.3f' % (np.mean(scores),
                                         np.std(scores)))