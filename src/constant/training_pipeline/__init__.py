import numpy as np

LOCAL_DATA_FILE_PATH = (
    "/home/vinay/code/Development/code_base/NetworkSecurity/data/phisingData.csv"
)

SCHEMA_FILE_PATH = "data_schema/schema.yaml"


"""
Data ingetion constants 
"""

DATA_INGESTION_DIR: str = "data_ingestion"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_TRAIN_AND_SPLIT_RATIO: float = 0.2
DATA_INGESTION_DATABESE_NAME: str = "Projects"
DATA_INGESTION_COLLECTION_NAME: str = "phishing_data"


"""
Common constants for the traning pipeline
"""
TRAINING_PIPELINE_NAME: str = "training_pipeline"
TARGET_COLUMN: str = "result"
TRAINING_PIPELINE_DIR: str = "training_pipeline"
TRAINING_PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR_NAME: str = "artifact"
DATA_FILE_NAME: str = "phishing_data.csv"
TRAIN_DATA_FILE_NAME: str = "train.csv"
TEST_DATA_FILE_NAME: str = "test.csv"
RAW_DATA_FILE_NAME: str = "raw_data.csv"


"""Data validation constants"""
DATA_VALIDATION_DIR: str = "data_validation"
DATA_VALIDATION_VALID_DIR_NAME: str = "validation"
DATA_VALIDATION_VALID_DIR: str = "valid"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
DATA_VALIDATION_VALID_TEST_FILE_NAME: str = "test_file.csv"
DATA_VALIDATION_VALID_TRAIN_FILE_NAME: str = "train_file.csv"
DATA_VALIDATION_INVALID_TEST_FILE_NAME: str = "invalid_test_file.csv"
DATA_VALIDATION_INVALID_TRAIN_FILE_NAME: str = "invalid_train_file.csv"


"""Data Transformation constants"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_FILE_NAME: str = "preprocessor.joblib"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_FILE_NAME: str = "transformed_train.npy"
DATA_TRANSFORMATION_TRANSFORMED_TEST_FILE_NAME: str = "transformed_test.npy"


IMPUTER_PARAMS: dict = {
    "n_neighbors": 5,
    "weights": "uniform",
    "missing_values": np.nan,
    "metric": "nan_euclidean",
}


"""Model Training"""
MODEL_TRANING_DIR_NAME = "model_training"
MODEL_TRANING_MODEL_FILE_NAME = "model.joblib"

FINAL_MODEL_PATH="/home/vinay/code/Development/code_base/NetworkSecurity/final_model/model.pkl"


"""Cloud Storage"""
LOCAL_ARTIFACT_DIR: str = "artifact"
S3_BUCKET_NAME: str = "netsectesting"
S3_ARTIFACT_PREFIX: str = "artifacts"
