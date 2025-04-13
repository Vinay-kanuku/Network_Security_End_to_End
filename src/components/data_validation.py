from entity.config_entity import DataValidationConfig, DataIngestionConfig,TrainingPipelineConfig
from entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from utils.get_schema import generate_schema, export_schema_to_yaml, read_schema_from_yaml
import logging 
import os
import sys
import pandas as pd
import json
from constant.training_pipeline import SCHEMA_FILE_PATH
from components.data_ingestion import DataIngestion
from exception.custom_exception import NetworkException

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.schema_file_path = SCHEMA_FILE_PATH
        self.schema = read_schema_from_yaml(self.schema_file_path)

    def validate_data(self):
        """
        Validate the data by comparing the schema with the data.
        """ 
        try:
            # Load the data from the ingested files
            train_data = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_data = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            # Validatte the schema against the data 
            schema = read_schema_from_yaml(self.schema_file_path)
            
            for column in schema:
                if column not in train_data.columns:
                    raise ValueError(f"Column {column} not found in train data.")
                if column not in test_data.columns:
                    raise ValueError(f"Column {column} not found in test data.")
                
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise NetworkException(e, sys)
        
    def initiate_data_validation(self):
        pass 
        

    
if __name__ == "__main__":
    traning_pipelin_conf = TrainingPipelineConfig()
    config = traning_pipelin_conf.get_data_ingestion_config()
    data_inge = DataIngestion()
    data_ingestion_artifact = data_inge.initiate_data_ingestion()
    validation = DataValidation(data_ingestion_artifact, config)
    # validation.initiate_data_validation()
    validation.validate_data()

 


