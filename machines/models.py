from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC


classifiers = {
    "forest" : RandomForestClassifier(n_estimators=200,
                                      min_samples_leaf=0.63,
                                      max_depth= 6),
                                          
    "Tree": DecisionTreeClassifier(max_depth=6, 
                                   min_samples_leaf=0.55,
                                   random_state=123),
    
    "SVM": LinearSVC()
}

print("Success.")