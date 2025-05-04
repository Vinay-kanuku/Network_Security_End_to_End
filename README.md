# NetworkSecurity ML Pipeline

An end-to-end, production-ready Machine Learning pipeline for detecting potential threats in network environments. Built with modular architecture, full traceability, and CI/CD integration, this project is designed for scale, maintainability, and rapid iteration.

---

##  Project Overview

This repository captures the complete ML system lifecycle—from data ingestion to model deployment—targeting cloud-native infrastructure (AWS). It emphasizes:

* Clean OOP-based architecture
* Modular, testable components
* Version control and reproducibility
* Real-time deployment readiness

---

##  Tech Stack

| Layer                   | Technology                                 |
| ----------------------- | ------------------------------------------ |
| **Language**            | Python 3.11                                |
| **Architecture**        | Custom OOP-based ML pipeline (modularized) |
| **Data Source**         | MongoDB (NoSQL)                            |
| **Experiment Tracking** | MLflow (hosted via DAGsHub)                |
| **Model Registry**      | MLflow Registry                            |
| **Cloud Storage**       | AWS S3 (via Boto3)                         |
| **Error Handling**      | Custom `NetworkException` Class            |
| **Logging**             | CustomLogger (Python logging wrapper)      |
| **Orchestration**       | Python scripts (ZenML planned)             |
| **Deployment**          | Docker + AWS ECR + EC2 + GitHub Actions    |
| **UI**                  | Streamlit                                  |

---

## ✅ Completed Modules

### 1. **Data Ingestion**

* Connects to MongoDB and pulls raw network traffic data
* Drops unnecessary fields (e.g., `_id`)
* Splits into train/test datasets with timestamp versioning
* Stores in structured `artifact/` directories

### 2. **Data Validation**

* Schema-driven validation logic (column checks, dtype checks)
* Detects missing/unexpected columns
* Generates validation reports with logs
* Raises structured exceptions via `NetworkException`

### 3. **Data Transformation**

* Implements Scikit-learn pipelines
* Handles scaling, encoding, and transformations
* Saves transformers for downstream inference compatibility
* Version-controlled artifacts with metadata

### 4. **Model Training**

* Modular trainer class for reusability
* Supports hyperparameterized model fitting
* Logs metrics to MLflow
* Stores serialized model artifacts

### 5. **Experiment Tracking**

* Integrated with MLflow hosted via DAGsHub
* Logs: parameters, metrics, artifacts, tags
* Supports model registration, stage transitions (e.g., Production, Staging)

---

##  Deployment-Ready Features

###  Model Registry Integration

* Fetches best model from MLflow Model Registry (via DAGsHub)
* Enables stage transitions and versioning

###  S3 Integration

* Uploads best model artifact to AWS S3
* Uses `boto3` to manage S3 storage
* Tracks uploaded version in logs/metadata

###  Model Pusher Module

* Fetches production-ready model
* Uploads model to S3
* Designed for CLI and CI/CD workflows

---

##  Infrastructure Status

| Feature                      | Status         |
| ---------------------------- | -------------- |
| MLflow + DAGsHub Integration | ✅ Complete     |
| Model Registry Support       | ✅ Complete     |
| S3 Push via Boto3            | ✅ Complete     |
| Dockerized Deployment        | ✅ Complete     |
| GitHub Actions CI/CD         | ✅ Complete     |
| EC2 Deployment               | ✅ Complete     |
| Streamlit Interface          | ✅ Complete     |
| FastAPI Inference Endpoint   | 🚧 In Progress |
| Batch Inference Engine       | 🔜 Planned     |
| ZenML Orchestration          | 🔜 Planned     |
| Enhanced Dashboard           | 🔜 Planned     |

---

##  Highlights and Learnings

* **Modularity wins**: Each pipeline stage is its own class, built for reuse
* **Fail-safe engineering**: Custom error logging + typed exceptions improve debuggability
* **MLflow + DAGsHub**: Powerful combo for experiment tracking and version control
* **CI/CD Matters**: GitHub Actions enables fully automated ECR builds
* **AWS Free Tier**: EC2 + ECR + S3 deployment optimized to stay within limits

---

##  Local Setup Guide

```bash
git clone https://github.com/Vinay-kanuku/netsec-ml-pipeline.git
cd netsec-ml-pipeline

pip install --upgrade pip
pip install -r requirements.txt

streamlit run app.py
```

---

##  What's Next?

* [ ] FastAPI Endpoint for real-time scoring
* [ ] Batch Inference Engine for periodic evaluation
* [ ] ZenML orchestration for full DAG management
* [ ] Streamlit 2.0 dashboard (exploratory insights)
* [ ] Dockerized offline predictor (for cron jobs or CLI usage)

---