from rich import print

from catboost import CatBoostRegressor

from utils.load import load_data
from utils.preprocessing import clean_data
from utils.transformers import transform_data
from utils.data_split import split_data
#from utils.train import train_regressor


from regression.train import train_regressor, evaluate_model, pickle_regressor



params = {
    "iterations": 200,
    "max_depth": 5,
    "learning_rate": 0.1,
    "verbose": 0
}


if __name__ == "__main__":
    data = load_data("Train (1).csv")
    cleaned_data = clean_data(data)
    X, target = transform_data(data)
    X_train, X_test, y_train, y_test = split_data(X, y=target)
    model = train_regressor(CatBoostRegressor, X_train, y_train, **params)
    mse, rmse, r2_score = evaluate_model(model, X_test, y_test)
    pickle_regressor(model, r2_score, path="models") 