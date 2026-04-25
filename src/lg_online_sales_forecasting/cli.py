from __future__ import annotations

import argparse
from pathlib import Path

from .config import ForecastConfig
from .pipeline import run_forecast


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the LG online sales forecasting pipeline.")
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("submissions/sales_forecast_submission.csv"))
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = ForecastConfig(data_dir=args.data_dir, output_path=args.output, random_state=args.seed)
    run_forecast(config)
    print(f"Saved submission: {config.output_path}")


if __name__ == "__main__":
    main()
