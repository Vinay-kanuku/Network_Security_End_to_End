from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import TrainingPipelineConfig
from src.components.data_trasformation import DataTransformation
 
from src.components.model.model_trainer import ModelTrainer

if __name__ == "__main__":
    training_pipeline_conf = TrainingPipelineConfig()
    config = training_pipeline_conf.get_data_ingestion_config()
    data_inge = DataIngestion()
    data_ingestion_artifact = data_inge.initiate_data_ingestion()
    validation_config = training_pipeline_conf.get_data_validation_config()
    validation = DataValidation(data_ingestion_artifact, validation_config)
    validation_artifact = validation.initiate_data_validation()
    data_transformation_config = training_pipeline_conf.get_data_trasformation_config()
    data_transformation = DataTransformation(
        validation_artifact, data_transformation_config
    )
    trabsformation_artifact = data_transformation.initiate_data_transformation()
    # model traning 
    model_trainer_config = training_pipeline_conf.get_model_trainer_config()
    model_trainer = ModelTrainer(trabsformation_artifact, model_trainer_config)
    model_trainer_artifact = model_trainer.initiate_model_traing()
    print(model_trainer_artifact.test_accuracy)
    
    