# LG Online Sales Forecasting

> LG Aimers 3기 연계 DACON 온라인 해커톤에서 제품별 온라인 채널 판매량을 예측한 프로젝트입니다. 제품 메타데이터와 판매 이력을 함께 활용하는 시계열 예측 파이프라인을 구성했습니다.

## Overview

| Field | Details |
| --- | --- |
| Competition | 온라인 채널 제품 판매량 예측 AI 온라인 해커톤 |
| Period | 2023.08.01 - 2023.09.17 |
| Final Round | 2023.09.16 10:00 - 2023.09.17 16:00 |
| Host | LG AI Research |
| Platform | DACON |
| Result | Preliminary 12th / 747 teams, Final 24th / 43 teams |
| Team | 4 members, team member |
| Task | Product-level online sales forecasting |
| Related Activity | LG Aimers 3rd cohort |

## Approach

- Converted wide product-level sales history into a long time-series training table.
- Built lag features, rolling statistics, calendar cycles, and product metadata features.
- Trained a tabular forecasting model with log-transformed sales targets.
- Used recursive multi-step forecasting to fill the sample submission horizon.
- Provided notebooks and package-based forecasting code for reproducible submission generation.

## Forecasting Pipeline

```text
.
|-- notebooks/
|   |-- 01_data_overview.ipynb
|   `-- 02_forecasting_pipeline.ipynb
|-- src/lg_online_sales_forecasting/
|   |-- config.py
|   |-- data.py
|   |-- features.py
|   |-- modeling.py
|   |-- pipeline.py
|   |-- cli.py
|   `-- metrics.py
|-- requirements.txt
`-- pyproject.toml
```

## Run

Place DACON files under `data/`:

```text
data/
|-- train.csv
`-- sample_submission.csv
```

Run the forecasting pipeline:

```bash
pip install -r requirements.txt
PYTHONPATH=src python -m lg_online_sales_forecasting \
  --data-dir data \
  --output submissions/sales_forecast_submission.csv
```

## Repository Scope

This repository focuses on the forecasting workflow. Competition data, generated submissions, and model artifacts are excluded.

## Links

- [DACON competition page](https://dacon.io/competitions/official/236129/overview/description)
