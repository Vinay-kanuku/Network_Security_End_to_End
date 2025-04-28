import os
from datetime import datetime

from constant import training_pipeline as tp


class TrainingPipelineConfig:
    """
    A configuration class for the training pipeline.

    Attributes:
        artifact_name (str): The name of the artifact directory.
        artifact_dir (str): The path to the artifact directory, which is created using the provided timestamp.
        feature_store_dir (str): The path to the feature store directory within the artifact directory.
        ingested_dir (str): The path to the ingested data directory within the artifact directory.
        training_dir (str): The path to the training data file within the ingested directory.
        testing_dir (str): The path to the testing data file within the ingested directory.
        database_name (str): The name of the database used for data ingestion.
        collection_name (str): The name of the collection used for data ingestion.

    Args:
        timestamp (str): A timestamp string used to create unique directory paths. Defaults to the current timestamp
                         in the format "%Y-%m-%d-%H-%M-%S".
    """

    def __init__(
        self, timestamp: str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    ) -> None:
        self.artifact_name = tp.ARTIFACT_DIR_NAME
        self.artifact_dir = os.path.join(tp.ARTIFACT_DIR_NAME, timestamp)
        self.database_name = tp.DATA_INGESTION_DATABESE_NAME
        self.collection_name = tp.DATA_INGESTION_COLLECTION_NAME

    def get_data_ingestion_config(self):
        return DataIngestionConfig(self)

    def get_data_validation_config(self):
        return DataValidationConfig(self)

    def get_data_transformation_config(self):
        return DataTransformationConfig(self)

    def get_model_trainer_config(self):
        return ModelTrainerConfig(self)


class DataIngestionConfig:
    """
    Configuration class for data ingestion.

    This class initializes and stores configuration parameters required for the
    data ingestion process. It retrieves these parameters from the provided
    TrainingPipelineConfig object.

    Attributes:
        database_name (str): Name of the database to be used.
        collection_name (str): Name of the collection within the database.
        feature_store_dir (str): Directory path for storing feature data.
        ingested_dir (str): Directory path for storing ingested data.
        training_dir (str): Directory path for storing training data.
        testing_dir (str): Directory path for storing testing data.
        train_test_split_ratio (float): Ratio for splitting data into training
            and testing sets.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.artifact_dir = training_pipeline_config.artifact_dir
        self.data_ingestion_dir = os.path.join(self.artifact_dir, tp.DATA_INGESTION_DIR)
        self.feature_store_dir = os.path.join(
            self.data_ingestion_dir, tp.DATA_INGESTION_FEATURE_STORE_DIR
        )
        self.ingested_dir = os.path.join(
            self.data_ingestion_dir, tp.DATA_INGESTION_INGESTED_DIR
        )

        self.train_data_path = os.path.join(self.ingested_dir, tp.TRAIN_DATA_FILE_NAME)
        self.test_data_path = os.path.join(self.ingested_dir, tp.TEST_DATA_FILE_NAME)
        self.raw_data_path = os.path.join(self.feature_store_dir, tp.RAW_DATA_FILE_NAME)
        self.database_name = training_pipeline_config.database_name
        self.collection_name = training_pipeline_config.collection_name
        self.train_test_split_ratio = tp.DATA_INGESTION_TRAIN_AND_SPLIT_RATIO


class DataValidationConfig:
    """
    DataValidationConfig is a configuration class for managing paths and settings
    related to data validation in a machine learning pipeline.

    Attributes:
        artifact_dir (str): The root directory for storing artifacts generated during the pipeline.
        valid_dir (str): Directory path for storing valid data files.
        invalid_dir (str): Directory path for storing invalid data files.
        valid_train_file_path (str): File path for storing the valid training dataset.
        valid_test_file_path (str): File path for storing the valid testing dataset.
        invalid_train_file_path (str): File path for storing the invalid training dataset.
        invalid_test_file_path (str): File path for storing the invalid testing dataset.
        drift_report_path (str): File path for storing the data drift report.
        validation_status (bool or None): Status of the data validation process.
            It is None by default and can be updated during the validation process.

    Args:
        training_pipeline_config (TrainingPipelineConfig): An instance of TrainingPipelineConfig
            that provides the base artifact directory and other pipeline configurations.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.artifact_dir = training_pipeline_config.artifact_dir
        self.valid_dir = os.path.join(
            self.artifact_dir, tp.DATA_VALIDATION_DIR, tp.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_dir = os.path.join(
            self.artifact_dir, tp.DATA_VALIDATION_DIR, tp.DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path = os.path.join(
            self.valid_dir, tp.DATA_VALIDATION_VALID_TRAIN_FILE_NAME
        )
        self.valid_test_file_path = os.path.join(
            self.valid_dir, tp.DATA_VALIDATION_VALID_TEST_FILE_NAME
        )
        self.invalid_train_file_path = os.path.join(
            self.invalid_dir, tp.DATA_VALIDATION_INVALID_TRAIN_FILE_NAME
        )
        self.invalid_test_file_path = os.path.join(
            self.invalid_dir, tp.DATA_VALIDATION_INVALID_TEST_FILE_NAME
        )
        self.drift_report_path = os.path.join(
            self.artifact_dir,
            tp.DATA_VALIDATION_DIR,
            tp.DATA_VALIDATION_DRIFT_REPORT_DIR,
            tp.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )
        self.validation_status = None


class DataTransformationConfig:
    """
    Configuration class for data transformation process.
    Attributes:
        artifact_dir (str): The root directory for storing all artifacts
            related to the data transformation process.
        data_transformation_dir (str): The directory for storing data
            transformation-specific artifacts.
        trasformed_dir (str): The directory where transformed data files
            (train and test) are stored.
        trasformed_obj_dir (str): The directory where transformed object
            files are stored.
        trasformed_train_file_path (str): The file path for the transformed
            training data.
        trasformed_test_file_path (str): The file path for the transformed
            testing data.
        trasformed_obj_file_path (str): The file path for the transformed
            object file.
    Args:
        training_pipeline_config (TrainingPipelineConfig): The configuration
            object for the training pipeline, which provides the root
            artifact directory.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.artifact_dir = training_pipeline_config.artifact_dir
        self.data_transformation_dir = os.path.join(
            self.artifact_dir, tp.DATA_TRANSFORMATION_DIR_NAME
        )
        self.trasformed_dir = os.path.join(
            self.data_transformation_dir, tp.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR
        )
        self.trasformed_obj_dir = os.path.join(
            self.data_transformation_dir, tp.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR
        )
        self.transformed_train_file_path = os.path.join(
            self.trasformed_dir, tp.DATA_TRANSFORMATION_TRANSFORMED_TRAIN_FILE_NAME
        )
        self.transformed_test_file_path = os.path.join(
            self.trasformed_dir, tp.DATA_TRANSFORMATION_TRANSFORMED_TEST_FILE_NAME
        )
        self.transformed_obj_file_path = os.path.join(
            self.trasformed_obj_dir, tp.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_FILE_NAME
        )


class ModelTrainerConfig:
    """
    Configuration class for model training process.
    Attributes:
        artifact_dir (str): The root directory for storing all artifacts
            related to the model training process.
        model_trainer_dir (str): The directory for storing model training-specific artifacts.
        trained_model_file_path (str): The file path for the trained model file.
    Args:
        training_pipeline_config (TrainingPipelineConfig): The configuration
            object for the training pipeline, which provides the root
            artifact directory.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.artifact_dir = training_pipeline_config.artifact_dir
        self.model_trainer_dir = os.path.join(
            self.artifact_dir, tp.MODEL_TRANING_DIR_NAME
        )
        self.trained_model_file_path = os.path.join(
            self.model_trainer_dir, tp.MODEL_TRANING_MODEL_FILE_NAME
        )


if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    training_pipeline_config.get_data_ingestion_config()
