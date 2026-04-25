from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ForecastConfig:
    """Runtime configuration for the sales forecasting pipeline."""

    data_dir: Path = Path("data")
    output_path: Path = Path("submissions/sales_forecast_submission.csv")
    train_file: str = "train.csv"
    sample_submission_file: str = "sample_submission.csv"

    item_id_column: str = "ID"
    timestamp_column: str = "date"
    target_column: str = "sales"
    forecast_column: str = "prediction"

    lag_days: tuple[int, ...] = (1, 7, 14, 28)
    rolling_windows: tuple[int, ...] = (7, 14, 28)
    min_training_lag_days: int = 28
    random_state: int = 42
