from datetime import datetime
import os 
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
    def __init__(self, 
                 timestamp: str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) -> None:
        self.artifact_name = tp.ARTIFACT_DIR_NAME
        self.artifact_dir = os.path.join(tp.ARTIFACT_DIR_NAME,timestamp)
        self.feature_store_dir = os.path.join(self.artifact_dir, tp.DATA_INGESTION_FEATURE_STORE_DIR)
        self.ingested_dir = os.path.join(self.artifact_dir, tp.DATA_INGESTION_INGESTED_DIR)
        self.training_dir = os.path.join(self.ingested_dir, tp.TRAIN_DATA_FILE_NAME)
        self.testing_dir = os.path.join(self.ingested_dir, tp.TEST_DATA_FILE_NAME)
        self.database_name = tp.DATA_INGESTION_DATABESE_NAME
        self.collection_name = tp.DATA_INGESTION_COLLECTION_NAME

    def get_data_ingestion_config(self):
        return DataIngestionConfig(self)

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
        self.database_name = training_pipeline_config.database_name
        self.collection_name = training_pipeline_config.collection_name
        self.feature_store_dir = training_pipeline_config.feature_store_dir
        self.ingested_dir = training_pipeline_config.ingested_dir
        self.training_dir = training_pipeline_config.training_dir
        self.testing_dir = training_pipeline_config.testing_dir
        self.train_test_split_ratio = tp.DATA_INGESTION_TRAIN_AND_SPLIT_RATIO
        self.train_data_path = os.path.join(self.ingested_dir, tp.TRAIN_DATA_FILE_NAME)
        self.test_data_path = os.path.join(self.ingested_dir, tp.TEST_DATA_FILE_NAME)
        self.raw_data_path = os.path.join(self.feature_store_dir, tp.RAW_DATA_FILE_NAME)
         

 
if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    training_pipeline_config.get_data_ingestion_config()
     

