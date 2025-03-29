from pymongo import MongoClient  
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, ConfigurationError
import os
from logger.logger import logging
from exception.custome_excetion import NetworkException 
 # Fixed exception name
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
uri = os.getenv("MONGODB_URI")

class DataBaseConnection:
    """
    Manages the connection to a MongoDB database.
    """

    def __init__(self, uri: str = uri):
        """
        Initializes the database connection.
        """
        self.uri = uri
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """
        Establishes a connection to the MongoDB database.
        """
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.db = self.client["Projects"]
            self.collection = self.db["phishing_data"]
            logging.info("MongoDB connection established successfully.")

        except (ConnectionFailure, ConfigurationError) as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise NetworkException(f"Failed to connect to MongoDB: {e}")

    def close(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            logging.info("MongoDB connection closed.")

if __name__ == "__main__":
    db = DataBaseConnection()
    db.connect()