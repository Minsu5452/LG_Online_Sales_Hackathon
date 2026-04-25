from __future__ import annotations

import numpy as np


def normalized_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Normalized MAE for non-negative sales forecasting."""

    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    denominator = np.maximum(np.mean(np.abs(y_true)), 1e-8)
    return float(np.mean(np.abs(y_true - y_pred)) / denominator)
