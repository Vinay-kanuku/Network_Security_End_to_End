import mlflow 
import os 
from dotenv import load_dotenv
load_dotenv()

def connect_to_mlflow():
    """
    Connect to MLflow server.
    """
    model_uri = os.getenv("MLFLOW_MODEL_URI")
    mlfow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    mlflow.set_tracking_uri(mlfow_tracking_uri)
