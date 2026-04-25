from __future__ import annotations

import os
import random

import numpy as np
import pandas as pd

from .config import ForecastConfig
from .data import (
    load_competition_data,
    predictions_to_submission,
    sample_submission_to_long,
    wide_train_to_long,
)
from .features import build_future_features, build_training_frame, split_features_target
from .modeling import SalesForecastModel


def seed_everything(seed: int) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)


class SalesForecastPipeline:
    """Recursive product-level sales forecasting pipeline."""

    def __init__(self, config: ForecastConfig) -> None:
        self.config = config
        self.model = SalesForecastModel(config)

    def fit_predict(self, train: pd.DataFrame, sample_submission: pd.DataFrame) -> pd.DataFrame:
        seed_everything(self.config.random_state)

        train_long, metadata_columns = wide_train_to_long(train, self.config)
        future_long = sample_submission_to_long(sample_submission, train, metadata_columns, self.config)

        training_frame = build_training_frame(train_long, self.config)
        train_features, train_target = split_features_target(training_frame, self.config)
        self.model.fit(train_features, train_target)

        history = train_long.copy()
        predictions = []
        for forecast_date in sorted(future_long[self.config.timestamp_column].unique()):
            future_step = future_long[future_long[self.config.timestamp_column] == forecast_date].copy()
            future_features_frame = build_future_features(history, future_step, self.config)
            future_features, _ = split_features_target(future_features_frame, self.config)
            forecast = self.model.predict(future_features)

            predicted_step = future_step.copy()
            predicted_step[self.config.forecast_column] = forecast
            predictions.append(predicted_step[[self.config.item_id_column, "date_column", self.config.forecast_column]])

            history_step = future_step.copy()
            history_step[self.config.target_column] = forecast
            history = pd.concat([history, history_step], ignore_index=True, sort=False)

        prediction_frame = pd.concat(predictions, ignore_index=True)
        return predictions_to_submission(sample_submission, prediction_frame, self.config)


def run_forecast(config: ForecastConfig) -> pd.DataFrame:
    competition_data = load_competition_data(config)
    pipeline = SalesForecastPipeline(config)
    submission = pipeline.fit_predict(competition_data.train, competition_data.sample_submission)

    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(config.output_path, index=False)
    return submission
