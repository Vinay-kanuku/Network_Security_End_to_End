import os
import sys

import joblib
import numpy as np
from exception.custom_exception import NetworkException
from logger.logger import logger


def save_numpy_array(file_path: str, array: np.array):
    """
    Save a numpy array to a file.
    Args:
        file_path (str): The path to the file.
        array (np.array): The numpy array to save.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkException(e, sys)


def load_numpy_array(file_path: str) -> np.array:
    """
    Load a numpy array from a file.
    Args:
        file_path (str): The path to the file.
        rns:
        np.array: The loaded numpy array.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkException(e, sys)


def save_transformed_object(file_path: str, obj):
    """
    Save an object to a file using joblib.
    Args:
        file_path (str): The path to the file.
        obj: The object to save.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        joblib.dump(obj, file_path)
    except Exception as e:
        raise NetworkException(e, sys)


def load_transformed_object(file_path: str):
    """
    Load an object from a file using joblib's safe_load method with security checks.
    Args:
        file_path (str): The path to the file.
    Returns:
        obj: The loaded object.
    Raises:
        NetworkException: If file doesn't exist or validation fails
    """
    try:
        # Verify file exists and is a regular file
        if not os.path.isfile(file_path):
            raise NetworkException("File does not exist or is not a regular file", sys)

        # Check file permissions (readable only by owner)
        if os.name != "nt":  # Unix-like systems
            file_mode = os.stat(file_path).st_mode & 0o777
            if file_mode != 0o600:
                raise NetworkException("Insecure file permissions", sys)

        # Load file with restricted mode
        obj = joblib.load(file_path, mmap_mode="r")

        # Validate loaded object is not None
        if obj is None:
            raise NetworkException("Loaded object is invalid", sys)

        return obj

    except Exception as e:
        logger.error(f"Error loading transformed object from {file_path}: {str(e)}")
        raise NetworkException(e, sys)
