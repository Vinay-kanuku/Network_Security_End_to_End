import os

import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split

from database.db_connection import DataBaseConnection
from entity.artifact_entity import DataIngestionArtifact
from exception.custom_exception import NetworkException
from logger.logger import logger
from src.entity.config_entity import DataIngestionConfig


class DataIngestion:
    """A class for handling data ingestion operations from MongoDB to CSV files.

    This class manages the extraction of data from MongoDB and its subsequent splitting
    into training and testing datasets. It includes functionality for database connection
    management, data export, and file saving operations.

    Attributes:
        config: Configuration object containing data ingestion parameters
        db: Database connection object for MongoDB operations

    Methods:
        export_data_from_db():
            Exports data from MongoDB and returns it as a pandas DataFrame.

            Returns:
                pd.DataFrame: The data retrieved from MongoDB with '_id' column removed.

            Raises:
                NetworkException: For MongoDB connection, value, or general errors.

        save_train_test_data(data_frame: pd.DataFrame) -> DataIngestionArtifact:
            Splits the input DataFrame into training and testing sets and saves them to files.

            Args:
                data_frame (pd.DataFrame): The DataFrame to split and save.

            Returns:
                DataIngestionArtifact: Object containing paths to saved train and test files.

            Raises:
                NetworkException: For file operation errors.

        initiate_data_ingestion() -> DataIngestionArtifact:
            Orchestrates the complete data ingestion process.

            Returns:
                DataIngestionArtifact: Object containing paths to saved train and test files.

            Raises:
                NetworkException: For MongoDB, file operation, or general errors.

    """

    def __init__(self, ingestion_config: DataIngestionConfig):  # Fixed constructor
        self.config = ingestion_config
        self.db = None

    def export_data_from_db(self):
        try:
            # tria = TrainingPipelineConfig()
            # self.config = tria.get_data_ingestion_config()

            self.db = DataBaseConnection(self.config)
            self.db.connect()
            data = self.db.collection.find()
            data_frame = pd.DataFrame(list(data))

            # Drop the '_id' column if it exists
            if "_id" in data_frame.columns:
                data_frame.drop(columns=["_id"], inplace=True)
                logger.info("Dropped '_id' column from the DataFrame.")

            logger.info("Data fetched from MongoDB successfully.")
            return data_frame
        except pymongo.errors.PyMongoError as mongo_err:
            logger.error(f"MongoDB error while fetching data: {mongo_err}")
            raise NetworkException(f"MongoDB error while fetching data: {mongo_err}")
        except ValueError as value_err:
            logger.error(f"Value error while processing data: {value_err}")
            raise NetworkException(f"Value error while processing data: {value_err}")
        except Exception as e:
            logger.error(f"Unexpected error while fetching data from MongoDB: {e}")
            raise NetworkException(
                f"Unexpected error while fetching data from MongoDB: {e}"
            )
        finally:
            if hasattr(self, "db") and hasattr(self.db, "client") and self.db.client:
                try:
                    self.db.close()
                    logger.info("MongoDB connection closed.")
                except Exception as close_err:
                    logger.warning(
                        f"Error while closing MongoDB connection: {close_err}"
                    )

    def save_train_test_data(self, data_frame: pd.DataFrame) -> DataIngestionArtifact:
        """
        Splits the data into training and testing sets.
        """
        train_set, test_set = train_test_split(
            data_frame, test_size=self.config.train_test_split_ratio, random_state=42
        )
        logger.info("Data split into training and testing sets.")

        # Check if the paths are correctly formed
        logger.info(f"Train path: {self.config.train_data_path}")
        logger.info(f"Test path: {self.config.test_data_path}")

        # Make sure the directory structure exists
        # os.makedirs(os.path.dirname(self.config.data_ingestion_dir), exist_ok=True)
        os.makedirs(os.path.dirname(self.config.raw_data_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.config.train_data_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.config.test_data_path), exist_ok=True)
        logger.info("Directories for train and test data created.")

        # Save the files
        data_frame.to_csv(self.config.raw_data_path, index=False)
        logger.info("Raw data saved successfully.")
        train_set.to_csv(self.config.train_data_path, index=False)
        test_set.to_csv(self.config.test_data_path, index=False)
        logger.info("Train and test data saved successfully.")
        data_ingetion_artifact = DataIngestionArtifact(
            train_file_path=self.config.train_data_path,
            test_file_path=self.config.test_data_path,
        )

        return data_ingetion_artifact  # Return the split datasets

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the data ingestion process.
        """
        try:
            data_frame = self.export_data_from_db()
            data_ingestion_artifact = self.save_train_test_data(
                data_frame
            )  # Now correctly receives the return values
            logger.info("Data ingestion process completed successfully.")
            return data_ingestion_artifact
        except pymongo.errors.PyMongoError as mongo_err:
            logger.error(f"MongoDB error during data ingestion: {mongo_err}")
            raise NetworkException(f"MongoDB error during data ingestion: {mongo_err}")
        except FileNotFoundError as file_err:
            logger.error(f"File operation error during data ingestion: {file_err}")
            raise NetworkException(
                f"File operation error during data ingestion: {file_err}"
            )
        except Exception as e:
            logger.error(f"Unexpected error during data ingestion: {e}")
            raise NetworkException(f"Unexpected error during data ingestion: {e}")
        finally:
            if hasattr(self, "db") and hasattr(self.db, "client") and self.db.client:
                try:
                    self.db.client.close()
                    logger.info("MongoDB connection closed.")
                except Exception as close_err:
                    logger.warning(
                        f"Error while closing MongoDB connection: {close_err}"
                    )


if __name__ == "__main__":
    ob = DataIngestion()
    ob.initiate_data_ingestion()
