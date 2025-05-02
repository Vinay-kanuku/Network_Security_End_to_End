# NetworkSecurity ML Pipeline

An end-to-end, production-ready Machine Learning pipeline for detecting potential threats in network environments. Built with modular architecture, full traceability, and CI/CD integration, this project is designed for scale, maintainability, and rapid iteration.

---

## Project Overview

This repository captures a complete ML system lifecycle—from data ingestion to model registration, with deployment workflows targeting cloud-native infrastructure (AWS). It emphasizes version control, modularity, and extensibility to support real-world operations.

---

## Tech Stack

| Layer | Tech |
|------|------|
| Language | Python |
| Architecture | Custom OOP-based ML pipeline (modular) |
| Data Source | MongoDB (NoSQL) |
| Experiment Tracking | MLflow (hosted via DAGsHub) |
| Model Registry | MLflow Registry |
| Cloud Storage | AWS S3 |
| Error Handling | Custom `NetworkException` |
| Logging | CustomLogger (Python logging wrapper) |
| Orchestration | Python scripts (extensible to Airflow/ZenML) |
| Deployment | AWS S3 + Docker (ECR Ready) |
| CI/CD | GitHub Actions |

---

## Completed Modules

### 1. Data Ingestion
- Connects to MongoDB and pulls raw network data
- Drops irrelevant fields (e.g., `_id`)
- Splits into versioned train/test datasets
- Stores in time-stamped, traceable artifact directories

### 2. Data Validation
- Schema-driven validation logic
- Detects missing/unexpected columns
- Logs detailed mismatch reports
- Raises structured exceptions using `NetworkException`

### 3. Data Transformation
- Scikit-learn pipelines for preprocessing
- Supports standard scaling, encoding, and transformation
- Saves transformation pipeline for consistent inference
- Transformed data is artifacted and version-controlled

### 4. Model Training
- Modular trainer integration
- Handles data loading, model fitting, and serialization
- Saves models locally for downstream use

### 5. Experiment Tracking
- Integrated with MLflow hosted on DAGsHub
- Logs all metrics, parameters, and models
- Uses MLflow Model Registry for stage/version management

---

## Deployment-Ready Features

### Model Registry Integration
- Fetches best registered model from MLflow Registry via DAGsHub
- Supports versioning and model promotion to Production/Staging

### S3 Model Push
- Uploads best model artifact to AWS S3 using Boto3
- Supports both MLflow-native and raw model upload

### Model Pusher Module
- Fetches best model from registry
- Uploads to S3
- Designed to work in CLI or automated runner

---

## Infrastructure Readiness

| Feature | Status |
|--------|--------|
| MLflow + DAGsHub Integration | Complete |
| Model Registry (Best Model Fetch) | In progress|
| S3 Push via Boto3 | In progress |
| Dockerized for Deployment | In Progress |
| CI/CD via GitHub Actions | In Progress |
| API Endpoint (FastAPI) | Planned |

---

## Upcoming Features

- Batch Inference Engine
- FastAPI for real-time scoring
- ZenML orchestration support
- Streamlit-based visual dashboard
- Dockerized offline predictor (CLI and cron jobs)

---

## Local Setup Guide

Follow the steps below to set up the project locally:



```bash
git clone https://github.com/Vinay-kanuku/netsec-ml-pipeline.git
cd netsec-ml-pipeline

pip install --upgrade pip
pip install -r requirements.txt

streamlit run app.py
```