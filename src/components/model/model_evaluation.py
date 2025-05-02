from logger.logger import logger
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from src.exception.custom_exception import NetworkException


class ModelEvaluation:
    """
    A class for evaluating machine learning models on test data.

    This class provides functionality to evaluate trained models and select the best performing one
    based on validation scores, then evaluate it on test data.

    Attributes:
        None

    Methods:
        evaluate_models_on_test(best_models, report, X_test, y_test):
            Evaluates the best model from cross-validation on test data.

            Args:
                best_models (dict): Dictionary containing trained model objects.
                report (dict): Dictionary containing validation scores for each model.
                X_test: Test features.
                y_test: True labels for test data.

            Returns:
                dict: Dictionary containing:
                    - best_model_name (str): Name of the best performing model
                    - test_accuracy (float): Accuracy score on test data
                    - cv_score (float): Cross-validation score of the best model
                    - best_model: The best performing model object
    """

    def __init__(self, model, X_test, y_test, imputer):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.imputer = imputer

    def evaluate_models_on_test(self):
        try:
            logger.info("Evaluating models on test data")
            X_test_transformed = self.imputer.transform(self.X_test)
            y_pred = self.model.predict(X_test_transformed)
            test_accuracy = accuracy_score(self.y_test, y_pred)
            r2 = r2_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred)
            recall = recall_score(self.y_test, y_pred)
            f1 = f1_score(self.y_test, y_pred)
            roc_auc = roc_auc_score(self.y_test, y_pred)

            return {
                "test_accuracy": test_accuracy,
                "r2_score": r2,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "roc_auc": roc_auc,
            }
        except Exception as e:
            raise NetworkException(f"Model evaluation failed: {str(e)}")
