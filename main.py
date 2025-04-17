from src.components.data_ingestion import DataIngestion 
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import TrainingPipelineConfig
from src.exception.custom_exception import NetworkException
from src.components.data_trasformation import DataTransformation
 


if __name__ == "__main__":
 
    training_pipeline_conf = TrainingPipelineConfig()
    config = training_pipeline_conf.get_data_ingestion_config()
    data_inge = DataIngestion()
    data_ingestion_artifact = data_inge.initiate_data_ingestion()
    validation_config = training_pipeline_conf.get_data_validation_config()
    validation = DataValidation(data_ingestion_artifact, validation_config)
    validation_artifact = validation.initiate_data_validation()
    data_transformation_config = training_pipeline_conf.get_data_trasformation_config()
    data_transformation = DataTransformation(validation_artifact, data_transformation_config)
    trabsformation_artifact = data_transformation.initiate_data_transformation()
 






