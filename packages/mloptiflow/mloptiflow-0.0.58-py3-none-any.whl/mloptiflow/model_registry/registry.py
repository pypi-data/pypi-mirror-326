from pathlib import Path
from typing import Optional, Dict, Any
import mlflow
from mlflow.tracking import MlflowClient
from mloptiflow.utils.exceptions import PredictionError


class ModelRegistry:
    def __init__(self, tracking_uri: Optional[str] = None):
        self.tracking_uri = tracking_uri or "file:./mlruns"
        mlflow.set_tracking_uri(self.tracking_uri)
        self.client = MlflowClient()

    def get_latest_model(self, experiment_name: str, model_name: str = "XGBoost") -> Dict[str, Any]:
        experiment = self.client.get_experiment_by_name(experiment_name)
        if experiment is None:
            raise PredictionError(f"No experiment found with name: {experiment_name}")

        runs = self.client.search_runs(
            experiment_ids=[experiment.experiment_id],
            filter_string="status = 'FINISHED'",
            order_by=["start_time DESC"],
            max_results=1
        )

        if not runs:
            raise PredictionError("No successful runs found")

        run = runs[0]
        artifacts_dir = Path(run.info.artifact_uri).relative_to(Path(self.tracking_uri).parent)
        
        return {
            "run_id": run.info.run_id,
            "model_path": artifacts_dir / f"{model_name}_model",
            "scaler_path": artifacts_dir / "scaler"
        }

    def load_model(self, experiment_name: str, model_name: str = "XGBoost") -> Dict[str, Any]:
        model_info = self.get_latest_model(experiment_name, model_name)
        return mlflow.sklearn.load_model(str(model_info["model_path"]))
