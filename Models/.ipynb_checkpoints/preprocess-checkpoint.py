import pandas as pd

def separate(X):
    X.set_index('Tour_ID', inplace=True)
    
    y=[]
    num=[col for col in X.select_dtypes('int','float').columns]
    cat=[]
    text=[]
    for col in X.select_dtypes(['object', 'category']).columns:
        if col not in ['cost_category']:
            num_values=len(X[col].unique())
            
            if num_values<=6:
                cat.append(col)
            else:
                text.append(col)
        else:
            y.append(col)
                
    results=print(f"Target Column: {y}\n\nNumerical Columns: {num}\n\nCategorical Columns: {cat}\n\nText Columns: {text}")
    return results
    

def drop(X):
    col_drop= ['Tour_ID',]
    X= X.drop(columns=col_drop, axis=1)
    
    return X

def extra_features(data):
    data['total_nights']=data['night_mainland']+data['night_zanzibar']
    bins=[0,14,30,60,365]
    labels=['Normal','extended','longer', 'staycation']
    data['trip_length']=pd.cut(data['total_nights'], bins=bins, labels=labels).astype('object')
    
    data['total_people']=data['total_female']+data['total_male']
    bins=[0,5,10,15,100]
    labels=['small','big','bigger','massive']
    data['group_size']=pd.cut(data['total_people'], bins=bins, labels=labels).astype('object')
    
    data['main_activity']=data['main_activity'].replace('Widlife Tourism','Wildlife Tourism')
    
    return(data)