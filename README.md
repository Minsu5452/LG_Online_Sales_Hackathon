# 온라인 채널 제품 판매량 예측

LG Aimers 3기 연계 DACON 온라인 해커톤에서 제품별 온라인 채널 판매량을 예측한 시계열 프로젝트입니다.

## 개요

| 항목 | 내용 |
| --- | --- |
| 대회 | 온라인 채널 제품 판매량 예측 AI 온라인 해커톤 |
| 기간 | 2023.08.01 - 2023.09.17 |
| 주최 / 주관 | LG AI Research / DACON |
| 결과 | 예선 12등, 본선 24등 |
| 요약 표기 | 예선 Top 1.6%, 본선 진출 |
| 연계 활동 | LG Aimers 3기 |

## 접근

- wide 형식 판매 이력을 제품별 long 시계열 학습 테이블로 변환했습니다.
- lag, rolling statistics, calendar cycle, product metadata 피처를 구성했습니다.
- log 변환 타겟에 대해 tabular regression 모델을 학습했습니다.
- 재귀적 multi-step forecasting으로 제출 구간을 채웠습니다.

## 저장소 구성

```text
.
├── notebooks/
│   ├── 01_data_overview.ipynb
│   └── 02_forecasting_pipeline.ipynb
└── requirements.txt
```

## 공개 범위

대회 원본 데이터, 모델 파일, 제출 파일은 포함하지 않았습니다. 노트북 출력과 실행 메타데이터를 정리했습니다.

## 링크

- [DACON 대회 페이지](https://dacon.io/competitions/official/236129/overview/description)
