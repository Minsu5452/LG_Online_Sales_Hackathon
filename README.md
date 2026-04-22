# LG Online Sales Hackathon

LG AI Research가 주최한 판매량 예측 해커톤 저장소입니다. 제품 메타데이터와 시계열 판매 기록을 함께 사용해 transformer 기반 예측 모델을 구성했고, 예선 12위로 본선에 진출했습니다.

## Snapshot

| Item | Detail |
| --- | --- |
| Type | Competition solution |
| Period | 2023.08-2023.09 |
| Team | 4 people, team member |
| Result | Preliminary 12th / 747 teams, final 24th / 43 teams |
| Task | 온라인 채널 제품 판매량 회귀 예측 |
| Key approach | Transformer-based time-series modeling |

## Contribution

- 판매 이력과 제품 속성을 함께 사용하는 입력 구조를 정리했습니다.
- 결측 보정, 이상치 완화, 시간 피처 생성 등 전처리에 참여했습니다.
- transformer 기반 시계열 예측 실험과 결과 정리에 기여했습니다.
- 오프라인 본선 해커톤 환경에서 추가 실험을 진행했습니다.

## Repository Layout

- `Preprocess.ipynb`: 데이터 정제 및 입력 구성
- `Real_final_code_Transfomer.ipynb`: 최종 transformer 실험 노트북

## Links

- [DACON competition page](https://dacon.io/competitions/official/236129/overview/description)
