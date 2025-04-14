import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
from scipy.stats import ks_2samp

from components.data_ingestion import DataIngestion
from constant.training_pipeline import SCHEMA_FILE_PATH
from entity.artifact_entity import (DataIngestionArtifact,
                                    DataValidationArtifact)
from entity.config_entity import (DataIngestionConfig, DataValidationConfig,
                                  TrainingPipelineConfig)
from exception.custom_exception import NetworkException
from logger.logger import logger
from utils.get_schema import (export_schema_to_yaml, generate_schema,
                              read_schema_from_yaml)


class DataValidation:
    """
    Class for validating data against schema and generating drift reports.

    This class handles data validation tasks such as:
    - Validating columns against a schema
    - Detecting data drift between datasets
    - Generating validation artifacts

    Attributes:
        data_ingestion_artifact: Artifact from the data ingestion step
        data_validation_config: Configuration for data validation
        schema_file_path: Path to the schema file
        schema: Loaded schema from the schema file
    """

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        """
        Initialize the DataValidation class.

        Args:
            data_ingestion_artifact: Artifact from the data ingestion step
            data_validation_config: Configuration for data validation
        """
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.schema_file_path = SCHEMA_FILE_PATH
        self.schema = read_schema_from_yaml(self.schema_file_path)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Read data from a file.

        Args:
            file_path: Path to the file

        Returns:
            DataFrame containing the data

        Raises:
            NetworkException: If there's an error reading the file
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise NetworkException(e)

    def validate_columns(self, schema: Dict[str, Any], data: pd.DataFrame) -> bool:
        """
        Validate that all required columns from schema are present in the data.

        Args:
            schema: Dictionary containing the schema definition
            data: DataFrame to validate

        Returns:
            True if all required columns are present, False otherwise
        """
        # Get columns from schema and data
        schema_columns = set(
            key for col in schema.get("columns", []) for key in col.keys()
        )

        data_columns = set(data.columns)
        # return len(schema_columns - data_columns) == 0
        return len(schema_columns - data_columns) == 0

    def generate_drift_report(
        self, base_df: pd.DataFrame, cur_df: pd.DataFrame, threshold: float = 0.05
    ) -> Dict[str, Dict[str, Union[float, bool]]]:
        """
        Generate drift report between two dataframes using Kolmogorov-Smirnov test.

        This method compares each column in both dataframes to detect statistical
        differences that may indicate data drift.

        Args:
            base_df: Base dataframe (reference distribution)
            cur_df: Current dataframe to compare against base
            threshold: p-value threshold for drift detection (default: 0.05)

        Returns:
            Dictionary containing drift report with p-values and drift indicators
        """
        report = {}
        for column in base_df.columns:
            if column in cur_df.columns:
                d1 = base_df[column]
                d2 = cur_df[column]

                # Skip non-numeric columns
                if not pd.api.types.is_numeric_dtype(
                    d1
                ) or not pd.api.types.is_numeric_dtype(d2):
                    continue

                is_same_dist = ks_2samp(d1, d2)
                is_found_drift = True  # Corrected variable name

                if threshold <= is_same_dist.pvalue:
                    is_found_drift = False  # Corrected variable name

                report[column] = {
                    "p_value": float(is_same_dist.pvalue),
                    "drift": is_found_drift,
                }

        return report  # Fixed indentation to return after processing all columns

    def validate_data(self) -> Dict[str, Dict[str, Union[float, bool]]]:
        """
        Validate the data by comparing the schema with the data and generate drift report.

        This method:
        1. Loads train and test data
        2. Validates columns against schema
        3. Saves validated data to designated paths
        4. Generates and saves a drift report

        Returns:
            Drift report dictionary

        Raises:
            NetworkException: If validation fails or encounters errors
        """
        try:
            # Load the data from the ingested files
            train_data = self.read_data(self.data_ingestion_artifact.train_file_path)
            test_data = self.read_data(self.data_ingestion_artifact.test_file_path)

            # Validate the schema against the data
            schema = read_schema_from_yaml(self.schema_file_path)
            schema_columns = set(
                key for col in schema.get("columns", []) for key in col.keys()
            )

            # Check if the columns in the schema match the columns in the data
            status = self.validate_columns(schema, train_data)
            if not status:
                logger.error("Schema validation failed for training data.")
                missing_cols = schema_columns - set(train_data.columns)
                logger.info(f"Columns missing in training data: {missing_cols}")
                raise NetworkException(
                    f"Schema validation failed for training data {e}"
                )

            status = self.validate_columns(schema, test_data)
            if not status:
                logger.error("Schema validation failed for testing data.")
                missing_cols = schema_columns - set(test_data.columns)
                logger.info(f"Columns missing in testing data: {missing_cols}")
                raise NetworkException(f"Schema validation failed for testing data {e}")

            # Create directories for valid data files
            os.makedirs(
                os.path.dirname(self.data_validation_config.valid_train_file_path),
                exist_ok=True,
            )
            os.makedirs(
                os.path.dirname(self.data_validation_config.valid_test_file_path),
                exist_ok=True,
            )

            # Save valid data
            train_data.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )
            test_data.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            # Generate drift report
            base_df = self.read_data(
                self.data_ingestion_artifact.train_file_path
            )  # Fixed typo
            cur_df = self.read_data(self.data_ingestion_artifact.test_file_path)
            drift_report = self.generate_drift_report(base_df=base_df, cur_df=cur_df)

            if not drift_report:
                logger.error(
                    "Drift report generation failed or no numeric columns available for drift detection."
                )
                raise NetworkException(f"Drift report generation failed {e}")

            # Save the drift report to the artifact directory
            drift_report_path = self.data_validation_config.drift_report_path
            os.makedirs(os.path.dirname(drift_report_path), exist_ok=True)

            with open(drift_report_path, "w") as f:
                json.dump(drift_report, f, indent=4)

            logger.info(f"Drift report saved to {drift_report_path}")
            return drift_report

        except FileNotFoundError as e:
            logger.error(f"Error loading data: {e}")
            raise NetworkException(e)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            raise NetworkException(e, sys)
        except pd.errors.EmptyDataError as e:
            logger.error(f"Empty data error: {e}")
            raise NetworkException(e)
        except pd.errors.ParserError as e:
            logger.error(f"Parser error: {e}")
            raise NetworkException(e)
        except Exception as e:
            logger.error(f"Error in data validation: {e}")
            raise NetworkException(e)

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Initiate the data validation process.

        This method orchestrates the full data validation workflow and
        generates the appropriate artifacts with validation status.

        Returns:
            DataValidationArtifact containing validation results and file paths

        Raises:
            NetworkException: If validation process encounters errors
        """
        try:
            drift_report = self.validate_data()
            validation_status = bool(drift_report)

            os.makedirs(
                os.path.dirname(self.data_validation_config.invalid_test_file_path),
                exist_ok=True,
            )
            os.makedirs(
                os.path.dirname(self.data_validation_config.invalid_train_file_path),
                exist_ok=True,
            )
            if validation_status:
                logger.info("Data validation completed successfully.")

                return DataValidationArtifact(
                    validation_status=True,
                    validated_train_file_path=self.data_validation_config.valid_train_file_path,
                    validated_test_file_path=self.data_validation_config.valid_test_file_path,
                    drireport_file_path=self.data_validation_config.drift_report_path,
                    invalidated_train_file_path=self.data_validation_config.invalid_train_file_path,
                    invalidated_test_file_path=self.data_validation_config.invalid_test_file_path,
                )
            else:
                logger.error("Data validation failed - empty drift report.")

                return DataValidationArtifact(
                    validation_status=False,
                    validated_train_file_path=None,
                    validated_test_file_path=None,
                    drireport_file_path=self.data_validation_config.drift_report_path,
                    invalidated_train_file_path=self.data_validation_config.invalid_train_file_path,
                    invalidated_test_file_path=self.data_validation_config.invalid_test_file_path,
                )

        except Exception as e:
            logger.error(f"Error in data validation process: {e}")
            raise NetworkException(e)
        finally:
            logger.info("Data validation process completed.")


if __name__ == "__main__":
    # Test the data validation component
    training_pipeline_conf = TrainingPipelineConfig()
    config = training_pipeline_conf.get_data_ingestion_config()
    data_inge = DataIngestion()
    data_ingestion_artifact = data_inge.initiate_data_ingestion()

    validation_config = training_pipeline_conf.get_data_validation_config()
    validation = DataValidation(data_ingestion_artifact, validation_config)
    validation_artifact = validation.initiate_data_validation()
