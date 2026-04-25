from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .config import ForecastConfig


def build_regressor(config: ForecastConfig):
    try:
        from lightgbm import LGBMRegressor

        return LGBMRegressor(
            n_estimators=600,
            learning_rate=0.03,
            num_leaves=63,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=config.random_state,
            objective="regression_l1",
            verbose=-1,
        )
    except ImportError:
        return HistGradientBoostingRegressor(
            loss="absolute_error",
            learning_rate=0.05,
            max_iter=300,
            random_state=config.random_state,
        )


class SalesForecastModel:
    """Tabular lag-feature model with log-target transformation."""

    def __init__(self, config: ForecastConfig) -> None:
        self.config = config
        self.model: TransformedTargetRegressor | None = None

    def fit(self, features: pd.DataFrame, target: pd.Series) -> "SalesForecastModel":
        numeric_columns = features.select_dtypes(include=["number", "bool"]).columns.tolist()
        categorical_columns = [column for column in features.columns if column not in numeric_columns]

        preprocessor = ColumnTransformer(
            transformers=[
                ("numeric", SimpleImputer(strategy="median"), numeric_columns),
                (
                    "categorical",
                    Pipeline(
                        steps=[
                            ("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                        ]
                    ),
                    categorical_columns,
                ),
            ],
            remainder="drop",
        )

        regressor = Pipeline(
            steps=[
                ("preprocess", preprocessor),
                ("model", build_regressor(self.config)),
            ]
        )

        self.model = TransformedTargetRegressor(
            regressor=regressor,
            func=np.log1p,
            inverse_func=np.expm1,
            check_inverse=False,
        )
        self.model.fit(features, target.clip(lower=0))
        return self

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        if self.model is None:
            raise RuntimeError("Model is not fitted.")
        return np.maximum(self.model.predict(features), 0)
