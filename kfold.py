def skfold(classification_model:str, sample:str, y, kfold):
    
    results={"model_name": f"{classification_model}_{sample}",
            "f1_score": []}
    
    #results['model name']= classification_model+ "_" + sample
    
    model=classification_model
    X= sample
    
    for fold, (train_idx,val_idx) in enumerate(kfold.split(X,y)):
        X_train, X_val= X[train_idx], X[val_idx]
        y_train, y_val=y[train_idx], y[val_idx]
    
        
        model.fit(X_train, y_train)
        y_pred=model.predict(X_val)
        
        f1 = f1_score(y_val, y_pred)
        results["f1_scores"].append(f1)
        results[f"kfold_{fold+1}"] = f1
        
        results["mean_f1"] = sum(results["f1_scores"]) / len(results["f1_scores"])
    return results
    
    
    