from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

class GreedySelection:
    def score(self, X, y):
        model = LogisticRegression(penalty='l2', solver='lbfgs',
                                  max_iter=1000, multi_class='ovr')
        model.fit(X, y)
        preds = model.predict_proba(X)
        auc = roc_auc_score(y, preds, multi_class='ovr')
        
        return auc
    
    def feature_selection(self, X, y):
        scoring_features = []
        best_scores = []
        
        no_of_features = X.shape[1]
        
        while True:
            
            this_feature = None
            best_score = 0
            
            for feature in range(no_of_features):
                if feature in scoring_features:
                    continue
            
            selected_features = scoring_features + [feature]
            
            xtrain = X[:, selected_features]
            
            score = self.score(xtrain, y)
            
            if score > best_score:
                this_feature = feature
                best_score = score
            
            if this_feature != None:
                scoring_features.append(this_feature)
                best_scores.append(best_score)
                
            if len(best_scores) > 2:
                if best_scores[-1] < best_scores[-2]:
                    break
                    
        return best_scores[:-1], scoring_features[:-1]
    
    def __call__(self, X, y):
        score, features = self.feature_selection(X, y)
        
        return X[:, features], score