from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ForecastConfig


RESERVED_COLUMNS = {"date", "sales", "prediction", "date_column"}


def add_calendar_features(frame: pd.DataFrame, config: ForecastConfig) -> pd.DataFrame:
    enriched = frame.copy()
    timestamp = enriched[config.timestamp_column]
    enriched["year"] = timestamp.dt.year
    enriched["month"] = timestamp.dt.month
    enriched["day"] = timestamp.dt.day
    enriched["day_of_week"] = timestamp.dt.dayofweek
    enriched["week_of_year"] = timestamp.dt.isocalendar().week.astype(int)
    enriched["is_weekend"] = enriched["day_of_week"].isin([5, 6]).astype(int)
    enriched["month_sin"] = np.sin(2 * np.pi * enriched["month"] / 12)
    enriched["month_cos"] = np.cos(2 * np.pi * enriched["month"] / 12)
    enriched["dow_sin"] = np.sin(2 * np.pi * enriched["day_of_week"] / 7)
    enriched["dow_cos"] = np.cos(2 * np.pi * enriched["day_of_week"] / 7)
    return enriched


def add_lag_features(frame: pd.DataFrame, config: ForecastConfig) -> pd.DataFrame:
    featured = frame.sort_values([config.item_id_column, config.timestamp_column]).copy()
    grouped_sales = featured.groupby(config.item_id_column)[config.target_column]

    for lag in config.lag_days:
        featured[f"lag_{lag}"] = grouped_sales.shift(lag)

    shifted_sales = grouped_sales.shift(1)
    for window in config.rolling_windows:
        rolling = shifted_sales.groupby(featured[config.item_id_column]).rolling(window=window, min_periods=1)
        featured[f"rolling_mean_{window}"] = rolling.mean().reset_index(level=0, drop=True)
        featured[f"rolling_std_{window}"] = rolling.std().reset_index(level=0, drop=True).fillna(0)

    return featured


def build_training_frame(train_long: pd.DataFrame, config: ForecastConfig) -> pd.DataFrame:
    featured = add_lag_features(add_calendar_features(train_long, config), config)
    required_lag = f"lag_{config.min_training_lag_days}"
    if required_lag in featured.columns:
        featured = featured.dropna(subset=[required_lag])
    return featured.dropna(subset=[config.target_column]).reset_index(drop=True)


def build_future_features(history: pd.DataFrame, future_step: pd.DataFrame, config: ForecastConfig) -> pd.DataFrame:
    future = future_step.copy()
    future[config.target_column] = np.nan

    combined = pd.concat([history, future], ignore_index=True, sort=False)
    featured = add_lag_features(add_calendar_features(combined, config), config)
    return featured.loc[featured[config.target_column].isna()].copy()


def split_features_target(frame: pd.DataFrame, config: ForecastConfig) -> tuple[pd.DataFrame, pd.Series]:
    target = frame[config.target_column]
    features = frame[get_model_feature_columns(frame, config)].copy()
    return features, target


def get_model_feature_columns(frame: pd.DataFrame, config: ForecastConfig) -> list[str]:
    reserved = {
        config.timestamp_column,
        config.target_column,
        config.forecast_column,
        "date_column",
    }
    return [column for column in frame.columns if column not in reserved]
