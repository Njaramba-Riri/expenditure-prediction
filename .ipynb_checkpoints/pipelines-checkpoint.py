from preprocess import separate
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.feature_extraction import DictVectorizer


def preprocessor(X):
    cat=[]
    text=[]
    for col in X.select_dtypes(['object', 'category']).columns:
        if col not in ['cost_category']:
            num_values=len(X[col].unique())
            
            if num_values<=10:
                cat.append(col)
            else:
                text.append(col)
    num= [col for col in X.select_dtypes('int','float').columns]
             
    num_pipeline=Pipeline([
        ("imputer", KNNImputer(n_neighbors=3)),
        ("scaler", StandardScaler()),
    ])
    
    cat_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("encoder", OneHotEncoder(sparse_output=False)),
    ])
    
    text_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("vectorizer",DictVectorizer(sparse=True, dtype=float)),
    ])
    
    preprocessor=ColumnTransformer([
        ("cat", cat_pipeline, cat),
        ("num", num_pipeline, num),
        ("text", text_pipeline, text),
    ])

    pipe=Pipeline([("preprocessor", preprocessor)])

    return pipe.fit_transform(X)


def preprocessor2(X): 
    cat=[]
    text=[]
    for col in X.select_dtypes(['object', 'category']).columns:
        if col not in ['cost_category']:
            num_values=len(X[col].unique())
            
            if num_values<=6:
                cat.append(col)
            else:
                text.append(col)
        num= [col for col in X.select_dtypes('int','float').columns]
     
      
        num_pipeline=Pipeline([
            ("imputer", SimpleImputer(strategy='median')),
            ("scaler", MinMaxScaler())
        ])
        
        cat_pipeline=Pipeline([
            ("imputer", SimpleImputer(strategy='most_frequent')),
            ("ohe", OneHotEncoder()),
        
        ])
        
        text_pipeline=Pipeline([
            ("imputer", SimpleImputer(strategy='most_frequent')),
            ("encoder", OrdinalEncoder()),
        ])
    
        preprocessor=ColumnTransformer([
            ("cat", cat_pipeline, cat),
            ("num", num_pipeline, num),
            ("text", text_pipeline, text),
        ])
    
        pipe=Pipeline([("preprocessor", preprocessor)])
    
    return pipe.fit_transform(X)


"""
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin

class TextSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]

class NumericSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[[self.key]]

class CategoricalSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[[self.key]]

text = Pipeline([
                ('selector', TextSelector(key='text')),
                ('tfidf', TfidfVectorizer())
            ])

numeric = Pipeline([
                ('selector', NumericSelector(key='numeric')),
                ('scaler', StandardScaler())
            ])

categorical = Pipeline([
                ('selector', CategoricalSelector(key='categorical')),
                ('onehot', OneHotEncoder())
            ])

features = FeatureUnion([
            ('text', text),
            ('numeric', numeric),
            ('categorical', categorical)
            ])

pipeline = Pipeline([
            ('features', features),
            ('model', model)
            ])

"""
