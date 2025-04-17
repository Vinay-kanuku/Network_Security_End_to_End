
from exception.custom_exception import NetworkException
from logger.logger import logger 
import os 
import sys 
import numpy as np
import pickle 

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
    Save an object to a file.
    Args:
        file_path (str): The path to the file.
        obj: The object to save.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise NetworkException(e, sys)
    
def load_transformed_object(file_path: str):
    """
    Load an object from a file.
    Args:
        file_path (str): The path to the file.
        rns:
        obj: The loaded object.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkException(e, sys)
    