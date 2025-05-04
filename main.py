
from src.pipeline.training_pipeline import TrainingPipeline

if __name__ == "__main__":
    # pipeline = TrainingPipeline()
    # model_trainer_artifact = pipeline.run_pipeline()
    # print(f"Test Accuracy: {model_trainer_artifact.test_accuracy}")
    ob = TrainingPipeline().run_pipeline()
  
    
    
    