# LG Online Sales Forecasting

> LG Aimers 3기 연계 DACON 온라인 해커톤에서 제품별 온라인 채널 판매량을 예측한 프로젝트입니다. 제품 메타데이터와 판매 이력을 함께 활용하는 시계열 예측 파이프라인을 구성했습니다.

## Overview

| 항목 | 내용 |
| --- | --- |
| 대회 | 온라인 채널 제품 판매량 예측 AI 온라인 해커톤 |
| 예선 (온라인) | 2023.08.01 ~ 2023.08.28 |
| 본선 (오프라인 해커톤) | 2023.09.16 ~ 2023.09.17 |
| 주최 | LG AI Research |
| 주관 | DACON |
| 결과 | 예선 12등 / 747팀, 본선 24등 / 43팀 |
| 팀 구성 | 4인팀, 팀원 |
| 과제 | 제품별 온라인 채널 판매량 예측 |
| 연계 활동 | LG Aimers 3기 |

## Approach

- 제품별 wide 형식 판매 이력을 long 시계열 학습 테이블로 변환했습니다.
- lag, rolling 통계, 캘린더 사이클, 제품 메타데이터 피처를 구성했습니다.
- log 변환된 타겟에 대해 tabular 회귀 모델을 학습했습니다.
- 재귀적 다단계 forecasting 으로 sample submission 의 예측 구간을 채웠습니다.

## Repository Structure

```text
.
├── notebooks/
│   ├── 01_data_overview.ipynb
│   └── 02_forecasting_pipeline.ipynb
├── requirements.txt
└── README.md
```

## Public Scope

이 저장소는 포트폴리오 공개용으로 정리한 버전입니다.

- 대회 제공 데이터, 제출 CSV, 학습된 모델 파일은 포함하지 않았습니다.
- 노트북 출력 결과와 실행 메타데이터는 제거했습니다.
- 더미 Transformer 실험 노트북과 외부 참고 노트북은 별도 보관소로 분리했습니다.
- 실행하려면 DACON 대회 데이터를 `data/` 경로에 별도로 배치해야 합니다.

## Links

- [DACON competition page](https://dacon.io/competitions/official/236129/overview/description)
