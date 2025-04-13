import pandas as pd 
from numpy import dtype
from logger import logger 
from exception.custom_exception import NetworkException
from numpy import dtype
import sys 
from schema import Schema, And, Use
from constant.training_pipeline import LOCAL_DATA_FILE_PATH, SCHEMA_FILE_PATH
import yaml 
def generate_schema(df: pd.DataFrame) -> dict:
    """
    Generate a schema for the given DataFrame.  
    Args:
        df (pd.DataFrame): The DataFrame for which to generate the schema.
        rns:
        dict: A dictionary containing the schema information.
    """ 
    try:
        schema = {"columns": []}    
        for column in df.columns:
            dtype = df[column].dtype
            if pd.api.types.is_string_dtype(dtype):
                schema["columns"].append({column:"str"})
            elif pd.api.types.is_numeric_dtype(dtype):
                schema["columns"].append({column:"int"})
            else:
                raise NetworkException(f"Unsupported dype {dtype} ", sys)
        return schema
    except Exception as e:
        raise NetworkException(e, sys)

def export_schema_to_yaml(schema: dict, file_path: str):
    """
    Export the schema to a YAML file.
    Args:
        schema (dict): The schema to export.
        file_path (str): The path to the YAML file.
    """
    try:
        with open(file_path, 'w') as file:
            yaml.dump(schema, file, default_flow_style=False, indent=2)
    except Exception as e:
        raise NetworkException(e, sys)
    
def read_schema_from_yaml(file_path: str) -> dict:
    """
    Read the schema from a YAML file.
    Args:
        file_path (str): The path to the YAML file.
    Returns:
        dict: The schema.
    """
    try:
        with open(file_path, 'r') as file:
            schema = yaml.safe_load(file)
        return schema
    except Exception as e:
        raise NetworkException(e, sys)

if __name__ == "__main__":
    df = pd.read_csv(LOCAL_DATA_FILE_PATH)
    schema = generate_schema(df)
    print(schema)
    export_schema_to_yaml(schema, SCHEMA_FILE_PATH)
    # print(schema)

 
    

 

   