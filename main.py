
from src.pipeline.training_pipeline import TrainingPipeline
from src.pipeline.prediction_pipeline import PredictionPipeline

if __name__ == "__main__":
    # pipeline = TrainingPipeline()
    # model_trainer_artifact = pipeline.run_pipeline()
    # print(f"Test Accuracy: {model_trainer_artifact.test_accuracy}")
    ob = PredictionPipeline()
    ob.run_prediction_pipeline()
    print("Prediction pipeline executed successfully.")
    
    
    