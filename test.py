from src.utils.model_training import load_pickle
import joblib
    

    # return X_train, y_train, X_test, y_test

path = "/home/vinay/code/Development/code_base/NetworkSecurity/artifact/2025-04-26-17-00-38/data_transformation/transformed_object/preprocessor.joblib"

imuter = load_pickle(path)
print(dir(imuter))