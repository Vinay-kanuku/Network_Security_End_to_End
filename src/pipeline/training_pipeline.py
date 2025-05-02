 

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model.model_trainer import ModelTrainer
from src.entity.config_entity import TrainingPipelineConfig

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def run_pipeline(self):
 
        data_ingestion_config = self.training_pipeline_config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

     
        data_validation_config = self.training_pipeline_config.get_data_validation_config()
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
 
        data_transformation_config = self.training_pipeline_config.get_data_transformation_config()
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

    
        model_trainer_config = self.training_pipeline_config.get_model_trainer_config()
        model_trainer = ModelTrainer(data_transformation_artifact, model_trainer_config)
        model_trainer_artifact = model_trainer.initiate_model_training()

        return model_trainer_artifact

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    model_trainer_artifact = pipeline.run_pipeline()
    print(f"Test Accuracy: {model_trainer_artifact.test_accuracy}")