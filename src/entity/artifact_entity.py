from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """
    Artifact class for data ingestion.
    This class holds the paths to the training and testing datasets after ingestion.
    """

    train_file_path: str
    test_file_path: str

    def __post__init__(self):
        if not self.train_file_path or not self.test_file_path:
            raise ValueError("train_file_path and test_file_path must be provided.")


@dataclass
class DataValidationArtifact:
    """
    Artifact class for data validation.
    This class holds the paths to the training and testing datasets after validation.
    """

    validation_status: bool
    validated_train_file_path: str
    validated_test_file_path: str
    invalidated_train_file_path: str
    invalidated_test_file_path: str
    drireport_file_path: str

    def __post__init__(self):
        if not self.validated_train_file_path or not self.validated_test_file_path:
            raise ValueError(
                "validated_train_file_path and validated_test_file_path must be provided."
            )


@dataclass
class DataTransformationArtifact:
    """
    Artifact class for data transformation.
    This class holds the paths to the training and testing datasets after transformation.
    """

    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str

    def __post__init__(self):
        if not self.transformed_train_file_path or not self.transformed_test_file_path:
            raise ValueError(
                "transformed_train_file_path and transformed_test_file_path must be provided."
            )


@dataclass
class ModelTrainerArtifact:
    """
    Artifact class for model training.
    This class holds the paths to the trained model and its evaluation metrics.
    """

    trained_model_file_path: str
    r2_score: float
    precesion_score: float
    recall_score: float
    f1_score: float
    roc_auc_score: float
    test_accuracy: float
