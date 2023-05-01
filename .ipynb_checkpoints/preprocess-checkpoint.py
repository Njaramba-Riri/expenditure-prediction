import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def separate(X):
    num=col in X.select_dtypes('int','object').columns
    cat=[]
    text=[]
    for col in X.select_dtypes(['object', 'category']).columns:
        if col not in ['cost_category']:
            num_values=len(X[col].unique())
            
            if num_values<=6:
                cat.append(col)
            else:
                text.append(col)
                
    results=print(f"Numerical Columns: {num}\n\nCategorical Columns: {cat}\n\nText Columns: {text}")
    return results
  
    
def preprocessor(X):              
    num_pipeline=Pipeline([
        ("imputer", KNNImputer(n_neighbors=3)),
        ("scaler", StandardScaler())
    ])
    cat_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("encoder", OneHotEncoder(sparse=False)),
        
    ])
    text_pipeline=([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("vectorizer", CountVectorizer())
    ])
    
    preprocessor=ColumnTransformer([
        ("cat", cat_pipeline, cat),
        ("num", num_pipeline, num),
        ("text", text_pipeline, text),
    ])
    
    pipe=Pipeline([
        ("preprocessor", preprocessor)
    ])
    
    return pipe.fit_transform(X)



def preprocessor2(X):        
    num_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='median')),
        ("scaler", MinMaxScaler())
    ])
    cat_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("encoder", OneHotEncoder(sparse=False)),
        
    ])
    text_pipeline=([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("vectorizer", TfidfVectorizer())
    ])
    
    preprocessor=ColumnTransformer([
        ("cat", cat_pipeline, cat),
        ("num", num_pipeline, num),
        ("text", text_pipeline, text),
    ])
    
    pipe=Pipeline([
        ("preprocessor", preprocessor)
    ])
    
    return pipe.fit_transform(X)
