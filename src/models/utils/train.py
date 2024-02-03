from typing import Tuple, Annotated
from rich import  print

import math
import numpy as np 

from sklearn.linear_model import LinearRegression, Ridge, ElasticNet, RANSACRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def train_regressor(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> Tuple[
    Annotated[float, "Mean Error"],
    Annotated[float, "Squared Error"],
    Annotated[float, "R2 Score"]
]:
    models = {
        "Linear": LinearRegression(),
        "Ridge": Ridge(),

        "Forest": RandomForestRegressor(n_estimators=300,
                                        max_depth=5,
                                        criterion="absolute_error",
                                        random_state=42,
                                        n_jobs=-1)
        }
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        train_pred = model.predict(X_train)
        test_mse = mean_squared_error(y_test, y_pred)
        train_mse = mean_squared_error(y_train, train_pred)
        rmse = math.sqrt(test_mse)
        r2 = r2_score(y_test, y_pred)

        print(f"\n\nModel: {name}\nTrain MSE: {train_mse}\nTest MSE: {test_mse}\nRMSE: {rmse}\nR2: {r2}")
    return test_mse, rmse, r2