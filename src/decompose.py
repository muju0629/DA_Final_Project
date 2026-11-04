"""인구구성(분모 효과) 분해: shift-share, 연령 표준화."""
from __future__ import annotations

import numpy as np
import pandas as pd


def shift_share(pop0, rate0, pop1, rate1) -> pd.DataFrame:
    """취업자 변화 ΔE = 인구효과 + 고용률효과 + 교차항.

    pop0, pop1 : 기준·비교 시점 연령구간별 인구 (Series, index=연령구간)
    rate0, rate1 : 연령구간별 고용률 (0~1 비율)
    """
    for values in (pop0, rate0, pop1, rate1):
        if not values.index.is_unique or set(values.index) != set(pop0.index):
            raise ValueError("인구와 고용률의 연령구간은 중복 없이 일치해야 합니다.")
        if values.empty or values.isna().any() or not np.isfinite(values).all():
            raise ValueError("분해 입력에 빈 자료·결측값·무한대가 있습니다.")
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
    if (base_pop.empty or base_pop.isna().any() or not base_pop.index.is_unique
            or not np.isfinite(base_pop).all() or (base_pop < 0).any()
            or base_pop.sum() <= 0):
        raise ValueError("기준인구는 중복 없는 연령구간의 유한한 비음수 값이며 합이 양수여야 합니다.")
    weights = base_pop / base_pop.sum()
    # 일부 연령구간이 결측인 시점은 가중합을 계산하지 않는다.
    return (rates[weights.index] * weights).sum(axis=1, skipna=False)
