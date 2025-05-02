import os

import mlflow
import numpy as np

model_uri = os.getenv("MLFLOW_MODEL_URI")
mlfow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(mlfow_tracking_uri)


def predict(data):
    """Main function for command line usage"""

    data1 = [
        1,
        1,
        1,
        1,
        1,
        -1,
        0,
        1,
        1,
        1,
        1,
        1,
        -1,
        0,
        0,
        -1,
        -1,
        -1,
        0,
        1,
        1,
        1,
        1,
        -1,
        1,
        1,
        1,
        1,
        -1,
        -1,
        1,
    ]
    data2 = [
        1,
        0,
        1,
        1,
        1,
        -1,
        -1,
        -1,
        1,
        1,
        1,
        -1,
        -1,
        0,
        -1,
        -1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        -1,
        -1,
        0,
        -1,
        1,
        0,
        1,
        -1,
    ]
    features = list(data)
    data = np.array(features, dtype=np.float64).reshape(1, 30)
    # The model is logged with an input example
    pyfunc_model = mlflow.pyfunc.load_model(model_uri)
    op = pyfunc_model.predict(data)
    # if op[0] == 1:
    #     print("The URL is Phishing")
    # else:
    #     print("The URL is Legitimate")
    return op[0]


if __name__ == "__main__":
    predict()
