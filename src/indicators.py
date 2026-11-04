"""고용지표 계산식 (국가데이터처 정의 기준) + 프로젝트 확장지표.

입력 단위는 모두 '명' 또는 '천 명'으로 통일되어 있어야 한다.
"""
from __future__ import annotations

import pandas as pd


def unemployment_rate(unemployed, labor_force):
    """공식 실업률 = 실업자 / 경제활동인구 × 100"""
    return unemployed / labor_force * 100


def supplementary_indicators(
    unemployed,
    labor_force,
    time_related_underemployed,
    potential_available,
    potential_jobseekers,
) -> pd.DataFrame:
    """고용보조지표 1·2·3.

    Parameters
    ----------
    unemployed : 실업자
    labor_force : 경제활동인구
    time_related_underemployed : 시간관련추가취업가능자 (주 36시간 미만 + 추가취업 희망·가능)
    potential_available : 잠재취업가능자 (4주 구직했으나 취업 불가능)
    potential_jobseekers : 잠재구직자 (구직 안 했으나 취업 희망·가능)
    """
    potential_lf = potential_available + potential_jobseekers
    extended_lf = labor_force + potential_lf
    return pd.DataFrame(
        {
            "official": unemployed / labor_force * 100,
            "supp1": (time_related_underemployed + unemployed) / labor_force * 100,
            "supp2": (unemployed + potential_lf) / extended_lf * 100,
            "supp3": (time_related_underemployed + unemployed + potential_lf) / extended_lf * 100,
        }
    )


def extended_indicators(
    unemployed,
    labor_force,
    time_related_underemployed,
    potential_lf,
    rested_not_potential,
    job_prep_not_counted,
) -> pd.DataFrame:
    """프로젝트 자체 확장지표 4·5.

    rested_not_potential : '쉬었음' 중 잠재경활에 포함되지 않은 인원
    job_prep_not_counted : 비경활 취업준비자 중 위 어느 범주에도 포함되지 않은 인원
    → 두 값 모두 원자료에서 개인별로 상태를 하나씩만 배정해 중복을 제거한 뒤 넣을 것
    """
    base_num = time_related_underemployed + unemployed + potential_lf
    base_den = labor_force + potential_lf
    ext4_num = base_num + rested_not_potential
    ext4_den = base_den + rested_not_potential
    ext5_num = ext4_num + job_prep_not_counted
    ext5_den = ext4_den + job_prep_not_counted
    return pd.DataFrame(
        {
            "ext4": ext4_num / ext4_den * 100,
            "ext5": ext5_num / ext5_den * 100,
        }
    )


def validate_against_published(recalc: pd.Series, published: pd.Series, tol: float = 0.1) -> pd.DataFrame:
    """재계산값과 공표값 비교. 반올림 오차(tol %p)를 넘는 행을 표시한다."""
    out = pd.DataFrame({"recalc": recalc, "published": published})
    out["diff"] = (out["recalc"] - out["published"]).round(3)
    out["exceeds_tol"] = out["diff"].abs() > tol
    return out


def rse_confidence_interval(unemployed, labor_force, rse: float, z: float = 1.96) -> pd.DataFrame:
    """실업자 수 RSE로 실업률 95% 신뢰구간을 근사한다 (경활인구 오차는 무시하는 단순 근사).

    rse : 상대표준오차 (예: 0.03 = 3%). 청년 RSE 공표치가 없으므로 여러 값으로 민감도 분석할 것.
    """
    rate = unemployed / labor_force * 100
    half = z * rse * rate
    return pd.DataFrame({"rate": rate, "lower": rate - half, "upper": rate + half, "half_width": half})
