# 데이터 출처

AI 노출도 분석에 쓰는 파일만 저장소에 포함한다. 모두 2026-11-11에 받았고 원본은 수정하지 않았다. 자세한 확인 내용은 [`docs/ai_exposure_design_eda.md`](../docs/ai_exposure_design_eda.md) 1-4절에 있다.

| 파일 | 출처 | 이용 조건 |
|---|---|---|
| `raw/kosis/DT_1ES3B28J_직업중분류x연령_2013H1-2026H1.csv` | 국가데이터처 KOSIS, 지역별고용조사 「전국 직업/연령/교육정도/종사상지위별 취업자」(`DT_1ES3B28J`). 파일명만 바꿈 | 미확인 |
| `raw/kosis/DT_1DA7002S_연령별_경제활동인구_월_201301-202610.csv` | 국가데이터처 KOSIS, 경제활동인구조사 「연령별 경제활동인구 총괄」(`DT_1DA7002S`). 2026-11-23에 받음. 파일명만 바꿈 | 미확인 |
| `raw/ilo_wp140/Final_Scores_ISCO08_Gmyrek_et_al_2025.xlsx` | Gmyrek, P. 외 (2025). *Generative AI and Jobs: A Refined Global Index of Occupational Exposure*. ILO Working Paper 140. © ILO. https://doi.org/10.54394/HETP0387 (파일: https://github.com/pgmyrek/2025_GenAI_scores_ISCO08) | CC BY 4.0 |
| `raw/epoch_eci/eci_scores.csv` | Epoch AI, "Epoch Capabilities Index". https://epoch.ai/eci | CC BY 4.0 |
| `raw/ksco_isco/한국표준직업분류(KSCO 8차)-국제표준직업분류(ISCO-08) 연계표_20251103085955.xlsx` | 국가데이터처 통계분류포털 연계표 게시판 (2025-11-03 게시) | 미확인 |
| `processed/panel_mid.csv`, `processed/eci_ref.csv` | 위 자료로 `notebooks/07_ai_exposure_eda.ipynb`가 만듦 | — |
| `processed/panel_analysis.csv`, `processed/panel_analysis_codebook.csv` | `notebooks/08_ai_panel_preprocess.ipynb`가 만듦. 열 설명은 codebook 파일 | — |

ECI는 갱신될 때 과거 점수도 바뀌므로 이 파일(2026-11-11 기준)로 고정한다. MDIS 원자료는 저장소에 올리지 않는다.
