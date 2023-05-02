from preprocess import separate
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def preprocessor(X):
    cat=[]
    text=[]
    for col in X.select_dtypes(['object', 'category']).columns:
        if col not in ['cost_category']:
            num_values=len(X[col].unique())
            
            if num_values<=6:
                cat.append(col)
            else:
                text.append(col)
    num= col in X.select_dtypes('int','float').columns
             
    num_pipeline=Pipeline([
        ("imputer", KNNImputer(n_neighbors=3)),
        ("scaler", StandardScaler()),
    ])
    
    cat_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("encoder", OneHotEncoder(sparse=False)),
    ])
    
    text_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("vectorizer", CountVectorizer()),
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
    num= col in X.select_dtypes('int','float').columns
     
      
    num_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='median')),
        ("scaler", MinMaxScaler())
    ])
    cat_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("encoder", OneHotEncoder(sparse_output=False)),
        
    ])
    text_pipeline=Pipeline([
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("vectorizer", TfidfVectorizer()),
    ])
    
    preprocessor=ColumnTransformer([
        ("cat", cat_pipeline, cat),
        ("num", num_pipeline, num),
        ("text", text_pipeline, text),
    ])
    
    pipe=Pipeline([("preprocessor", preprocessor)])
    
    return pipe.fit_transform(X)