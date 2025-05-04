from sklearn.model_selection import RandomizedSearchCV

from logger.logger import logger
from src.utils.model_training import get_model_params


class HyperParameterTuning:
    """HyperParameterTuning class performs hyperparameter optimization for multiple machine learning models.

    This class handles the hyperparameter tuning process using RandomizedSearchCV for different
    classification models. It optimizes model parameters to find the best performing configuration.

    Methods:
        perform_hyperparameter_tuning(X_train, y_train): Performs hyperparameter tuning on multiple models.

    Attributes:
        None

    Example:
        tuner = HyperParameterTuning()
        report, best_models = tuner.perform_hyperparameter_tuning(X_train, y_train)
    """

    def __init__(self):
        pass

    def perform_hyperparameter_tuning(self, X_train, y_train):
        try:
            models, params = get_model_params()
            report = {}
            best_models = {}

            for model_name in models:
                model = models[model_name]
                param_grid = params[model_name]

                grid_search = RandomizedSearchCV(
                    estimator=model,
                    param_distributions=param_grid,
                    cv=5,
                    n_iter=10,
                    scoring="accuracy",
                    n_jobs=-1,
                    verbose=0,
                    random_state=42,
                )

                grid_search.fit(X_train, y_train)

                best_model = grid_search.best_estimator_  # model with best params
                best_score = grid_search.best_score_ # socre of the best model
                best_params = grid_search.best_params_ # params of the best model 

                report[model_name] = {"score": best_score, "best_params": best_params}

                best_models[model_name] = best_model

                logger.info(
                    f"[{model_name}] score: {best_score}, best_params: {best_params}"
                )

            return report, best_models

        except Exception as e:
            raise Exception(f"Model training failed: {str(e)}")
