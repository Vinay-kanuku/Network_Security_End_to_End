import asyncio

from components.model.prediction import predict
from exception.custom_exception import NetworkException
from utils.phishing_features import get_features


class PredictionPipeline:
    """
    A pipeline class for making predictions on network security data.

    This class implements a prediction pipeline that fetches features asynchronously
    and makes predictions using a pre-trained model.

    Methods:
        run_prediction_pipeline(): Execute the prediction pipeline by fetching features
                                 and making predictions.

    Returns:
        DataFrame: The prediction results after model inference.

    Raises:
        Exception: If any error occurs during feature fetching or prediction.
    """

    def __init__(self):
        pass

    def run_prediction_pipeline(self, url: str):
        try:
            data = asyncio.run(get_features(url))
            responce = predict(data)
            return responce
        except Exception as e:
            raise NetworkException(f"Error in prediction pipeline: {str(e)}")
