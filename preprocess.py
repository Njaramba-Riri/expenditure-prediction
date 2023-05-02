import pandas as pd

def separate(X):
    y=[]
    num= col in X.select_dtypes('int','float').columns
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
    
