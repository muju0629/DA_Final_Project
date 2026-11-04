"""프로젝트 공통 설정: 경로, 분석 기간, KOSIS 표 ID."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_EXTERNAL = ROOT / "data" / "external"
FIGURES = ROOT / "reports" / "figures"

# 잠정 분석 기간. 표별 제공 범위와 분류 개정·시계열 연속성을 확인한 뒤 확정한다.
START = "201501"
END = "202608"

# AI 분석 기준 시점 (ChatGPT 출시)
AI_SHOCK = "2022-12"

# KOSIS 표 ID (orgId=101, 국가데이터처)
# TODO: None 인 표와 '확인 필요' 표는 1주차에 KOSIS 화면에서 직접 확정
KOSIS_ORG_ID = "101"
TABLES = {
    "econ_pop_by_age": "DT_1DA7002S",       # 성/연령별 경제활동인구 (기존 후보; 사용 전 재확인)
    "supp_indicators_youth": None,          # 고용보조지표(청년층) — 확인 필요
    "inactive_by_activity": "DT_1DA7147S",  # 연령별 비경활 활동상태('쉬었음') — 확인 필요
    "emp_by_industry": "DT_1DA7E33S_NEW",   # 산업별 취업자 — 확인 필요
    "emp_by_occupation": "DT_1DA7E34S_NEW", # 직종별 취업자 — 확인 필요
}

YOUTH_AGE_GROUPS = ["15-19", "20-24", "25-29"]
COMPARE_AGE_GROUPS = ["30-39", "40-49", "50-59"]

# MDIS 원자료 가중치 환산 (천 명 단위 공표치와 일치시키기)
WEIGHT_DIVISOR_MONTHLY = 1_000
WEIGHT_DIVISOR_ANNUAL = 12_000
