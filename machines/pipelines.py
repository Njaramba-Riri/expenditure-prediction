#from preprocess import separate
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler, OrdinalEncoder, RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import itertools

def extra_features(df, categorical_cols):
    combi = list(itertools.combinations(categorical_cols, 2))
    
    for cat1, cat2 in combi:
        df.loc[:, cat1 + "_" + cat2] = df[cat1].astype(str) + "_" + df[cat2].astype(str)
    
    return df


def pipe(df):
    cat = []
    huge_cat = []
    num = [c for c in df.select_dtypes('int','float').columns]
    for col in df.select_dtypes(['object', 'category']).columns:
        num_values = len(df[col].unique())
        if num_values <= 20:
            cat.append(col)
        else:
            huge_cat.append(col)

        num_pipeline=Pipeline([
            ("imputer", SimpleImputer(strategy='median')),
            ("scaler", StandardScaler()),
        ])

        cat_pipeline=Pipeline([
            ("imputer", SimpleImputer(strategy='most_frequent')),
            ("encoder", OneHotEncoder(sparse_output=False)),
        ])

        lcat_pipeline=Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ("enc", OrdinalEncoder()),
        ])

        pipe=ColumnTransformer([ 
            ("cat", cat_pipeline, cat),
            ("num", num_pipeline, num),
            ("text", lcat_pipeline, huge_cat),
        ])

        tra = Pipeline([
            ('pipe', pipe),
            ('scaler', StandardScaler())
        ])
    

    return tra.fit_transform(df)


def pipe2(X):
    num= [c for c in X.select_dtypes('int','float').columns]
    cat=[]
    huge_cat=[]
    for col in X.select_dtypes(['object', 'category']).columns:
        num_values=len(X[col].unique())

        if num_values<=10:
            cat.append(col)
        else:
            huge_cat.append(col)


    num_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='median')),
        ("scaler", RobustScaler())
    ])

    cat_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("encoder", OrdinalEncoder()),
        ])

    lcat_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("encoder", OneHotEncoder(sparse_output=False)),
    ])

    pipe = ColumnTransformer([
        ("cat", cat_pipeline, cat),
        ("num", num_pipeline, num),
        ("text", lcat_pipeline, huge_cat)
    ])
    
    tra = Pipeline([
        ('pipe', pipe),
        ('scaler', StandardScaler()),
    
    ])
        
         
    return tra.fit_transform(X)


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
