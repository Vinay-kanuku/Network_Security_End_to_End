 
#  NetworkSecurity ML Pipeline
An end-to-end Machine Learning pipeline designed for detecting potential threats in network environments using structured data. The pipeline is modular, extensible, and aligned with best practices for production-grade ML systems.

##  Project Overview
This repository encapsulates a complete ML workflow starting from **data ingestion** through **validation** and now extending into **data transformation**, with upcoming plans for model training, evaluation, and deployment.

##  Tech Stack
- **Language:** Python
- **Pipeline Architecture:** Custom modular OOP-based design
- **Data Source:** MongoDB (NoSQL)
- **Logging:** CustomLogger (based on Python's `logging`)
- **Exception Handling:** Custom `NetworkException` class
- **Storage:** Local artifact directories (auto-versioned with timestamps)
- **Experiment Tracking:** MLFlow
- **CI/CD:** GitHub Actions
- **Containerization:** Docker
- **Cloud Deployment:** AWS (S3, ECR)

##  Completed Stages
### 1.  Data Ingestion
- Connects to MongoDB to fetch structured raw network data.
- Drops irrelevant fields such as `_id`.
- Splits data into **train** and **test** datasets.
- Stores datasets in a standardized artifact structure.

### 2.  Data Validation
- Validates train/test data against a **user-defined schema**.
- Checks for missing or unexpected columns.
- Logs detailed schema mismatch reports.
- Utilizes `NetworkException` for consistent error reporting (now fully integrated and fixed).

##  Upcoming Features
### 3.  Model Training & Evaluation
- Implementation of model trainer with customizable algorithms
- Hyperparameter tuning for optimal model performance
- Comprehensive evaluation metrics and validation

### 4.  Experiment Tracking
- MLFlow integration for experiment monitoring and comparison
- Remote repository connection via Dagshub for team collaboration
- Versioned model and experiment management

### 5.  Deployment Pipeline
- Model pusher implementation for production-ready artifacts
- End-to-end training pipeline automation
- Batch prediction capabilities for offline inference

### 6.  Cloud Infrastructure
- AWS S3 integration for model and artifact storage
- Containerization with Docker for consistent environments
- CI/CD automation with GitHub Actions for seamless deployment to AWS ECR

### 7.  Additional Tools
- Data Transformation (WIP)
- CLI Support & Configurable Runner
- FastAPI endpoint for real-time predictions