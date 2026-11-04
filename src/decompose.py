"""인구구성(분모 효과) 분해: shift-share, 연령 표준화."""
from __future__ import annotations

import pandas as pd


def shift_share(pop0, rate0, pop1, rate1) -> pd.DataFrame:
    """취업자 변화 ΔE = 인구효과 + 고용률효과 + 교차항.

    pop0, pop1 : 기준·비교 시점 연령구간별 인구 (Series, index=연령구간)
    rate0, rate1 : 연령구간별 고용률 (0~1 비율)
    """
    d_pop = pop1 - pop0
    d_rate = rate1 - rate0
    out = pd.DataFrame(
        {
            "population_effect": d_pop * rate0,
            "rate_effect": pop0 * d_rate,
            "interaction": d_pop * d_rate,
        }
    )
    out["total"] = out.sum(axis=1)
    out.loc["합계"] = out.sum()
    return out


def age_standardized_rate(rates: pd.DataFrame, base_pop: pd.Series) -> pd.Series:
    """연령 표준화 고용률 = Σ(기준연도 연령구간 인구비중 × 당해 연령구간 고용률).

    rates : index=날짜, columns=연령구간 (고용률)
    base_pop : 기준연도(예: 2015) 연령구간별 인구
    """
    weights = base_pop / base_pop.sum()
    return (rates[weights.index] * weights).sum(axis=1)
