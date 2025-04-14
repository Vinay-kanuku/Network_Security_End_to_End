
 

#  Dev README – NetworkSecurity ML Pipeline

>  Developer log of building a modular, production-aligned ML pipeline to detect network threats.  
 
> Author: Vinay (that’s me)  

---

##  Week 1 – Groundwork

### Day 1 – Project Setup [12/04/25]
- Setup the repo structure using modular folders: `components`, `pipelines`, `config`, `utils`, `logger`, etc.  
- Wrote a `CustomLogger` class using Python’s built-in logging (with timestamps, log rotation—will enhance later).  
- Created `NetworkException` class to have consistent, centralized exception handling across the pipeline.  
- Defined base configuration files to keep paths, schema locations, and artifacts clean.
- Implement data ingestion modue tmr 

### Day 2 – Data Ingestion Module [13/04/25]
- Connected to **MongoDB Atlas**, successfully pulled raw structured network logs.  
- Wrote ingestion logic to clean up unwanted fields (`_id`, timestamps, etc.).  
- Split dataset into train-test using stratified split logic (more future-proof).  
- Saved ingested datasets to `artifacts/data_ingestion` with timestamped folders (auto-versioned).  
- Logged every step (success, failure, edge cases). Ingestion solid .
- Data Validaion tmr 

### Day 3 – Data Validation [14/04/25] 
- Created user-defined schema in YAML to enforce strict column expectations.  
- Implemented `DataValidation` class to:
  - Check for column count mismatches
  - Missing/extra columns
  - Type mismatches (basic ones for now)  
- If schema mismatches → throws `NetworkException`, logged with stack trace + suggested fixes.  
- Fixed a bunch of early bugs here. Working clean now.  
- Logged comparison reports per run, dumped to `artifacts/data_validation`.
- Data Transformation tmr

### Data Transformation 
- Setup preprocessing pipeline using `scikit-learn`'s `Pipeline` and `ColumnTransformer`.  
- Scaling and standardization handled for numerical features.  
- Saved the preprocessing object using `joblib` to keep it consistent between training and inference.  
- Cleaned and transformed datasets saved as `transformed_train.csv` and `transformed_test.csv`.  
- TODO: Add imputation logic for missing values if needed later.

---

 

 

## 🚧 Upcoming
- Finish transformation unit tests and schema integrity checks  
- Start `ModelTrainer` module: make it flexible enough to test multiple algorithms  
- Integrate MLFlow and test with local server  
- Explore DagsHub repo link-up for remote experiment tracking  
- Plan FastAPI + Docker strategy early—deployment shouldn't be an afterthought

---

 