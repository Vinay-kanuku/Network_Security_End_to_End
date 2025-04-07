import os

# Fixed exception name
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ConnectionFailure
from pymongo.server_api import ServerApi
from exception.custom_exception import NetworkException
from entity.config_entity import DataIngestionConfig, TrainingPipelineConfig


from logger.logger import logger 

load_dotenv()

# Load environment variables
uri = os.getenv("MONGODB_URI")


class DataBaseConnection:
    """
    Manages the connection to a MongoDB database.
    """

    def __init__(self,config:DataIngestionConfig, uri:str=uri):
        """
        Initializes the database connection.
        """
        self.uri = uri
        self.client = None
        self.db = None
        self.collection = None
        self.config = config

    def connect(self):
        """
        Establishes a connection to the MongoDB database.
        """
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi("1"))
            self.db = self.client[self.config.database_name]
            self.collection = self.db[self.config.collection_name]
            logger.info("MongoDB connection established successfully.")

        except (ConnectionFailure, ConfigurationError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise NetworkException(f"Failed to connect to MongoDB: {e}")

    def close(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")


if __name__ == "__main__":
    pipeline = TrainingPipelineConfig()
    config = pipeline.get_data_ingestion_config()
    db = DataBaseConnection(config)
    db.connect()
    db.close()

