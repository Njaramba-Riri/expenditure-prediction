from zenml import pipeline
import mlflow

from steps.load_data import data_load
from steps.regressor.clean_data import data_clean
from steps.regressor.train_model import train_regressor
from steps.regressor.evaluate_model import evaluate_regressor

@pipeline(name="Regressor Pipeline", enable_cache=True, enable_artifact_metadata=True)
def run_regressor(data_path: str):
    data = data_load(data_path)
    X_train, X_test, y_train, y_test = data_clean(data)
    models = train_regressor(X_train, y_train)
    for model in models:
        mse_score, rmse_score, mae_score, r2_score = evaluate_regressor(model, X_test, y_test)
