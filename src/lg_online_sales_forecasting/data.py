from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .config import ForecastConfig


@dataclass(frozen=True)
class CompetitionData:
    train: pd.DataFrame
    sample_submission: pd.DataFrame


def load_competition_data(config: ForecastConfig) -> CompetitionData:
    train = pd.read_csv(config.data_dir / config.train_file)
    sample_submission = pd.read_csv(config.data_dir / config.sample_submission_file)
    return CompetitionData(train=train, sample_submission=sample_submission)


def infer_date_columns(frame: pd.DataFrame) -> list[str]:
    """Detect date-like wide columns such as `2022-01-01`."""

    date_columns: list[str] = []
    for column in frame.columns:
        if _is_date_like(column):
            date_columns.append(column)
    if not date_columns:
        raise ValueError("No date-like columns were found.")
    return date_columns


def infer_item_id_column(frame: pd.DataFrame, preferred_column: str) -> str:
    if preferred_column in frame.columns:
        return preferred_column
    return frame.columns[0]


def wide_train_to_long(train: pd.DataFrame, config: ForecastConfig) -> tuple[pd.DataFrame, list[str]]:
    date_columns = infer_date_columns(train)
    item_id_column = infer_item_id_column(train, config.item_id_column)
    metadata_columns = [column for column in train.columns if column not in {item_id_column, *date_columns}]

    long = train.melt(
        id_vars=[item_id_column, *metadata_columns],
        value_vars=date_columns,
        var_name=config.timestamp_column,
        value_name=config.target_column,
    )
    long = long.rename(columns={item_id_column: config.item_id_column})
    long[config.timestamp_column] = pd.to_datetime(long[config.timestamp_column])
    long[config.target_column] = pd.to_numeric(long[config.target_column], errors="coerce").fillna(0)
    long[config.target_column] = long[config.target_column].clip(lower=0)
    return long.sort_values([config.item_id_column, config.timestamp_column]).reset_index(drop=True), metadata_columns


def sample_submission_to_long(
    sample_submission: pd.DataFrame,
    train: pd.DataFrame,
    metadata_columns: list[str],
    config: ForecastConfig,
) -> pd.DataFrame:
    date_columns = infer_date_columns(sample_submission)
    train_id_column = infer_item_id_column(train, config.item_id_column)
    submission_id_column = infer_item_id_column(sample_submission, config.item_id_column)

    metadata = train[[train_id_column, *metadata_columns]].rename(columns={train_id_column: config.item_id_column})
    metadata = metadata.drop_duplicates(subset=[config.item_id_column])

    long = sample_submission.melt(
        id_vars=[submission_id_column],
        value_vars=date_columns,
        var_name="date_column",
        value_name=config.forecast_column,
    )
    long = long.rename(columns={submission_id_column: config.item_id_column})
    long[config.timestamp_column] = pd.to_datetime(long["date_column"])
    long = long.merge(metadata, on=config.item_id_column, how="left")
    return long.sort_values([config.timestamp_column, config.item_id_column]).reset_index(drop=True)


def predictions_to_submission(
    sample_submission: pd.DataFrame,
    predictions: pd.DataFrame,
    config: ForecastConfig,
) -> pd.DataFrame:
    submission = sample_submission.copy()
    submission_id_column = infer_item_id_column(submission, config.item_id_column)

    prediction_lookup = predictions.set_index([config.item_id_column, "date_column"])[config.forecast_column]
    date_columns = infer_date_columns(submission)

    for date_column in date_columns:
        keys = list(zip(submission[submission_id_column], [date_column] * len(submission)))
        submission[date_column] = [prediction_lookup.get(key, 0.0) for key in keys]

    return submission


def _is_date_like(value: object) -> bool:
    try:
        pd.to_datetime(str(value), errors="raise")
        return True
    except (ValueError, TypeError):
        return False
