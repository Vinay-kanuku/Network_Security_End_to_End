import dagshub
import joblib
import numpy as np
import pandas as pd
from exception.custom_exception import NetworkException
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from src.logger.logger import logger

dagshub.init(repo_owner="vinaykanuku7565", repo_name="netsec-ml-pipeline", mlflow=True)


def load_pickle(file_path: str):
    try:
        return joblib.load(file_path)
    except FileNotFoundError as e:
        raise NetworkException(f"File not found: {e}")
    except Exception as e:
        raise NetworkException(f"Error loading pickle file: {e}")
    except FileNotFoundError as e:
        raise NetworkException(f"File not found: {e}")
    except Exception as e:
        raise NetworkException(f"Error loading pickle file: {e}")


def get_model_params():
    models = {
        "RandomForestClassifier": RandomForestClassifier(),
        "KNeighborsClassifier": KNeighborsClassifier(),
        "LogisticRegression": LogisticRegression(),
        "SVC": SVC(),
        "DecisionTreeClassifier": DecisionTreeClassifier(),
    }

    params = {
        "RandomForestClassifier": {
            "n_estimators": [50, 100, 200],
            "max_depth": [10, 20, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
        },
        "KNeighborsClassifier": {
            "n_neighbors": [3, 5, 7, 9],
            "weights": ["uniform", "distance"],
            "p": [1, 2],  # Manhattan vs Euclidean
        },
        "LogisticRegression": {
            "C": [0.1, 1.0, 10, 100],
            "solver": ["liblinear", "saga"],
            "penalty": ["l1", "l2"],
            "max_iter": [100, 200],
        },
        "SVC": {
            "C": [0.1, 1, 10, 100],
            "kernel": ["linear", "rbf", "poly"],
            "gamma": ["scale", "auto"],
        },
        "DecisionTreeClassifier": {
            "max_depth": [10, 20, None],
            "min_samples_split": [2, 10],
            "min_samples_leaf": [1, 4],
            "criterion": ["gini", "entropy"],
        },
    }

    return models, params


def load_data(train_file_path, test_file_path):
    try:
        logger.info("Loading Data from artifacts")
        train_df = np.load(train_file_path)
        test_df = np.load(test_file_path)
        X_train = train_df[:, :-1]
        y_train = train_df[:, -1]
        X_test = test_df[:, :-1]
        y_test = test_df[:, -1]
        return X_train, y_train, X_test, y_test
    except FileNotFoundError as e:
        raise NetworkException(f"File not found: {e}")
    except pd.errors.EmptyDataError as e:
        raise NetworkException(f"Empty data: {e}")
    except pd.errors.ParserError as e:
        raise NetworkException(f"Parsing error: {e}")
    except Exception as e:
        raise NetworkException(f"Error loading data: {e}")
