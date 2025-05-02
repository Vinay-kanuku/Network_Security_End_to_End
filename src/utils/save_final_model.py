import mlflow
from mlflow.tracking import MlflowClient

# Replace with your Dagshub-hosted MLflow tracking URI
mlflow.set_tracking_uri("https://dagshub.com/vinaykanuku7565/netsec-ml-pipeline/mlflow")

client = MlflowClient()

# Replace with your experiment name or ID
experiment_name = "8b37a669fe02497f90012d6f6908712e"
experiment = client.get_experiment_by_name(experiment_name)

# Sort runs by descending accuracy (or any other metric)
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    filter_string="",
    run_view_type=1,  # active only
    order_by=["metrics.accuracy DESC"]
)

# Get the best run
best_run = runs[0]
best_run_id = best_run.info.run_id
print("Best run ID:", best_run_id)