from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    Artifact class for data ingestion.  
    This class holds the paths to the training and testing datasets after ingestion.
    """
    train_file_path: str
    test_file_path: str

    def __post__init__(self):
        if not self.train_file_path or not self.test_file_path:
            raise ValueError("train_file_path and test_file_path must be provided.")
        
@dataclass
class DataValidationArtifact:
    """
    Artifact class for data validation.
    This class holds the paths to the training and testing datasets after validation.
    """
    validation_status: bool
    validated_train_file_path: str
    validated_test_file_path: str
    invalidated_train_file_path: str
    invalidated_test_file_path: str
    drireport_file_path: str

    def __post__init__(self):
        if not self.validated_train_file_path or not self.validated_test_file_path:
            raise ValueError("validated_train_file_path and validated_test_file_path must be provided.")

    
 

 

 
 

 
