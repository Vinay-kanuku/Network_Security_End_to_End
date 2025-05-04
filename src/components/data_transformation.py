import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

from constant.training_pipeline import IMPUTER_PARAMS, TARGET_COLUMN
from entity.artifact_entity import (DataTransformationArtifact,
                                    DataValidationArtifact)
from entity.config_entity import DataTransformationConfig
from exception.custom_exception import NetworkException
from logger.logger import logger
from utils.data_tranformation import save_numpy_array, save_transformed_object


class DataTransformation:
    """
    Handles data transformation processes including:
    - Reading validated data
    - Imputing missing values
    - Combining features and target
    - Saving transformed data and the imputer object
    """

    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config

    def create_imputer_object(self, imputer_params: dict) -> KNNImputer:
        """
        Creates a KNNImputer object with provided parameters.
        """
        try:
            logger.info("Creating KNN Imputer object")
            imputer = KNNImputer(**imputer_params)
            return imputer
        except Exception as e:
            raise NetworkException(e)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Main transformation function: reads data, applies imputations, saves arrays & object.
        """
        try:
            logger.info("Initiating Data Transformation")

            # Load validated data
            train_df = pd.read_csv(
                self.data_validation_artifact.validated_train_file_path
            )
            test_df = pd.read_csv(
                self.data_validation_artifact.validated_test_file_path
            )

            # Initialize imputer
            imputer = self.create_imputer_object(imputer_params=IMPUTER_PARAMS)

            # Separate features and target
            train_features = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            test_features = test_df.drop(columns=[TARGET_COLUMN], axis=1)

            train_target = train_df[TARGET_COLUMN].replace(-1, 0)
            test_target = test_df[TARGET_COLUMN].replace(-1, 0)

            # Apply imputation
            transformed_train_features = imputer.fit_transform(train_features)
            transformed_test_features = imputer.transform(test_features)

            # Combine features and targets
            transformed_train = np.c_[transformed_train_features, train_target]
            transformed_test = np.c_[transformed_test_features, test_target]

            # Save arrays and transformation object
            save_numpy_array(
                self.data_transformation_config.transformed_train_file_path,
                transformed_train,
            )
            save_numpy_array(
                self.data_transformation_config.transformed_test_file_path,
                transformed_test,
            )
            save_transformed_object(
                self.data_transformation_config.transformed_obj_file_path, imputer
            )

            logger.info("Data Transformation Complete")

            # Return transformation artifact
            return DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_obj_file_path,
            )

        except Exception as e:
            raise NetworkException(e)
