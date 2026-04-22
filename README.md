# 📦 LG Online Sales Hackathon — 온라인 채널 제품 판매량 예측

![Preliminary](https://img.shields.io/badge/예선%20상위%201.6%25-12%2F747%20teams-brightgreen)
![Final](https://img.shields.io/badge/본선%2024%2F43-진출-blue)
![Host](https://img.shields.io/badge/Host-LG%20AI%20Research-red)
![Type](https://img.shields.io/badge/Type-온라인%20해커톤%20(1박2일%20오프라인)-orange)

> **예선 12위 / 747팀 (상위 1.6%) · 본선 24위 / 43팀** — LG AI Research 주최 공식 해커톤. **Transformer 기반 시계열 예측**으로 본선 진출. 예선 온라인 + 본선 **1박2일 오프라인** 해커톤.

---

## 🏆 Result

- 🏅 **예선 12위 / 747팀 (상위 1.6%)** · 2023.08.01 ~ 2023.08.28
- 🎯 **본선 24위 / 43팀** · 2023.09.16 ~ 2023.09.17 (1박2일 오프라인)
- 주최: LG AI Research / 주관: DACON
- 역할: 4인팀 (팀원)

## 🔍 Overview

- **배경**: 온라인 커머스의 제품별 판매량 예측은 재고·프로모션·물류 최적화의 핵심 지표.
- **문제 정의**: 제품 속성 + 시계열 판매 이력으로 **미래 N일 판매량(regression) 예측**.
- **난점**: 제품별 이질적 수요 패턴, 짧은 학습 시계열, 프로모션·주말 효과 혼재.

## 🧠 Approach

- **Transformer 기반 시계열 모델**: self-attention으로 장기 의존성 + 제품 embedding
- 피처: 판매 이력 윈도우 + 제품 메타데이터 + 시간 피처
- 전처리: 결측 보간, 이상치 스무딩, 카테고리 embedding

## 📈 Results

| 단계 | 순위 | 규모 | 비고 |
|------|------|------|------|
| 예선 | 12위 | 747팀 | 상위 1.6% |
| 본선 | 24위 | 43팀 | 본선 진출 |

## 🛠 Tech Stack

- Python 3.8+ · PyTorch · Transformer · Pandas · NumPy · Jupyter

## 📁 Structure

```
LG_Online_Sales_Hackathon/
├── Preprocess.ipynb
├── Real_final_code_Transfomer.ipynb   # 최종 Transformer 솔루션
└── README.md
```

## 🔗 Links

- [DACON 대회 페이지](https://dacon.io/competitions/official/236129/overview/description)

---

> 🔗 Portfolio: [Minsu5452](https://github.com/Minsu5452)
