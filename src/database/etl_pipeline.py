from db_connection import DataBaseConnection
import json
from csv import DictReader
from logger.logger import logging
from exception.custome_excetion import NetworkException
from abc import ABC, abstractmethod


class DataLoader(ABC):
    """Abstract class for data loaders."""
    @abstractmethod
    def load_data(self):
        pass




class CSVToJsonConverter(DataLoader):
    """Converts CSV data to JSON format."""
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def load_data(self):
        try:
            with open(self.csv_file, 'r') as file:
                reader = DictReader(file)
                data = list(reader)
                logging.info(f"Data converted to JSON format from {self.csv_file}")
                return data  # Returning a Python list, not a JSON string
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise NetworkException(f"File not found: {e}")
        except Exception as e:
            logging.error(f"Error converting data to JSON: {e}")
            raise NetworkException(f"Error converting data to JSON: {e}")


class JsonToMongoDB(DataLoader):
    """Inserts JSON data into MongoDB."""
    def __init__(self, db_connection, json_data, clear_before_insert=True):
        self.db_connection = db_connection
        self.json_data = json_data
        self.clear_before_insert = clear_before_insert


    def load_data(self):
        if self.clear_before_insert:
            self.db_connection.collection.delete_many({})
            logging.info("Existing data cleared from MongoDB collection.")
        
        if isinstance(self.json_data, list):
            try:
                self.db_connection.collection.insert_many(self.json_data)
                logging.info("Data inserted into MongoDB successfully.")
            except Exception as e:
                logging.error(f"Error inserting data into MongoDB: {e}")
                raise NetworkException(f"Error inserting data into MongoDB: {e}")
        else:
            logging.error("Invalid JSON data. Expected a list of dictionaries.")
            raise NetworkException("Invalid JSON data. Expected a list of dictionaries.")


class ETLPipeline:
    """ETL pipeline to load CSV data into MongoDB."""
    def __init__(self, db_connection, csv_file):
        self.db_connection = db_connection
        self.csv_file = csv_file

    def run(self):
        try:
            self.db_connection.connect()
            logging.info("ETL Pipeline started.")

            # Convert CSV to JSON
            json_data = CSVToJsonConverter(self.csv_file).load_data()

            # Insert JSON into MongoDB
            JsonToMongoDB(self.db_connection, json_data).load_data()

        except Exception as e:
            logging.error(f"ETL Pipeline failed: {e}")
            raise NetworkException(f"ETL Pipeline failed: {e}")
        finally:
            self.db_connection.close()


if __name__ == "__main__":
    db = DataBaseConnection()
    db.connect()
    csv_file = "/home/vinay/code/Development/code_base/NetworkSecurity/data/phisingData.csv"
    etl_pipeline = ETLPipeline(db, csv_file)
    etl_pipeline.run()