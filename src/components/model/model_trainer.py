import joblib
import mlflow
from exception.custom_exception import NetworkException
from logger.logger import logger
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.utils.model_training import load_data, load_pickle

from .hyper_params import HyperParameterTuning
from .model_evaluation import ModelEvaluation


class ModelTrainer:
    """
    A class for training machine learning models using provided data transformation artifacts and configuration.

    This class handles the complete model training pipeline including data loading, hyperparameter tuning,
    model training, evaluation and saving the trained model.

    Attributes:
        data_transformation_artifact (DataTransformationArtifact): Artifact containing transformed data paths
        model_trainer_config (ModelTrainerConfig): Configuration for model training process

    Methods:
        initiate_model_traing(): Initiates the model training process
        train_model(report, best_models, X_train, y_train): Trains the best selected model
        save_model(model): Saves the trained model to disk

    Raises:
        NetworkException: Custom exception for various errors during model training:
            - FileNotFoundError: When required files are not found
            - ValueError: For invalid values
            - TypeError: For type mismatches
            - KeyError: For missing dictionary keys
            - ImportError: For module import issues
            - General exceptions during training process

    Returns:
        ModelTrainerArtifact: Contains paths to trained model and various performance metrics
    """

    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def initiate_model_training(self) -> ModelTrainerArtifact:
        try:
            logger.info("Loading training and testing data from artifacts")
            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )
            X_train, y_train, X_test, y_test = load_data(
                train_file_path, test_file_path
            )
            report, best_models = HyperParameterTuning().perform_hyperparameter_tuning(
                X_train, y_train
            )
            model = self.train_model(report, best_models, X_train, y_train)
            imputer = load_pickle(
                self.data_transformation_artifact.transformed_object_file_path
            )
            metrics = ModelEvaluation(
                model, X_test, y_test, imputer
            ).evaluate_models_on_test()
            self.save_model(model)
            logger.info("Model training completed successfully")

            with mlflow.start_run():
                mlflow.log_params(report)
                mlflow.log_metrics(metrics)
                mlflow.sklearn.log_model(model, "model", input_example=X_train[0:1])

            return ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                test_accuracy=metrics["test_accuracy"],
                r2_score=metrics["r2_score"],
                precesion_score=metrics["precision"],
                recall_score=metrics["recall"],
                f1_score=metrics["f1"],
                roc_auc_score=metrics["roc_auc"],
            )
        except FileNotFoundError as e:
            raise NetworkException(f"File not found: {str(e)}")
        except ValueError as e:
            raise NetworkException(f"Value error: {str(e)}")
        except TypeError as e:
            raise NetworkException(f"Type error: {str(e)}")
        except KeyError as e:
            raise NetworkException(f"Key error: {str(e)}")
        except ImportError as e:
            raise NetworkException(f"Import error: {str(e)}")
        except Exception as e:
            raise NetworkException(f"Model training failed: {str(e)}")

    def train_model(
        self, report, best_models, X_train, y_train
    ) -> ModelTrainerArtifact:
        try:
            logger.info("Loading training and testing data from artifacts")
            best_model_name = max(report, key=lambda name: report[name]["score"])
            final_model = best_models[best_model_name]
            transformer = load_pickle(
                self.data_transformation_artifact.transformed_object_file_path
            )
            X_train_transformed = transformer.transform(X_train)
            final_model.fit(X_train_transformed, y_train)
            return final_model
        except Exception as e:
            raise NetworkException(f"Model training failed: {str(e)}")

    def save_model(self, model: ModelTrainerArtifact):
        try:
            logger.info("Saving the trained model")
            model_path = self.model_trainer_config.trained_model_file_path
            with open(model_path, "wb") as file:
                joblib.dump(model, file)
            logger.info(f"Model saved at {model_path}")
        except Exception as e:
            raise NetworkException(f"Model saving failed: {str(e)}")
        finally:
            logger.info("Model saving process completed")
            return model


if __name__ == "__main__":
    model_trainer_config = ModelTrainerConfig()
