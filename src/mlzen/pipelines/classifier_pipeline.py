from zenml import pipeline
from zenml.client import Client

from steps.load_data import data_load
from steps.classifier.clean_data import data_cleaning
from steps.classifier.train_model import model_train
from steps.classifier.evaluate_model import model_evaluate

@pipeline(name="classifier pipeline")
def run_classifier(data_path: str):
    df = data_load(data_path)
    X_train, X_test, y_train, y_test = data_cleaning(df)
    models = model_train(X_train, y_train, X_test, y_test)
    for model in models:
        pre_score, rec_score, roc_auc, f1 = model_evaluate(model, X_test, y_test)



# if __name__ == "__main__":
#     classifier_pipeline = classifier_pipeline.with_options(
#         run_name = "Expenditure Prediction_{{ date }}"
#     )

#     print(Client().active_stack.experiment_tracker.get_tracking_uri())
#     classifier_pipeline(data_path="Datasets/Train.csv")

