"""KOSIS OpenAPI 클라이언트.

가장 빠른 방법: KOSIS 웹에서 표를 연 뒤 'OpenAPI > URL 생성'으로 만든 주소를
그대로 fetch_url()에 넣는 것. 표마다 objL/itmId 파라미터가 달라 직접 조립하면 오류가 잦다.
"""
from __future__ import annotations

import os

import pandas as pd
import requests
from dotenv import load_dotenv

from .config import DATA_RAW, KOSIS_ORG_ID

load_dotenv()
BASE_URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"


def _api_key() -> str:
    key = os.getenv("KOSIS_API_KEY")
    if not key:
        raise RuntimeError(".env 에 KOSIS_API_KEY 를 설정하세요.")
    return key


def _to_frame(payload) -> pd.DataFrame:
    if isinstance(payload, dict) and "err" in payload:
        raise RuntimeError(f"KOSIS 오류 {payload.get('err')}: {payload.get('errMsg')}")
    df = pd.DataFrame(payload)
    if "DT" in df:
        df["DT"] = pd.to_numeric(df["DT"], errors="coerce")
    if "PRD_DE" in df:
        df["date"] = pd.to_datetime(df["PRD_DE"], format="%Y%m", errors="coerce")
    return df


def fetch_table(
    tbl_id: str,
    start: str,
    end: str,
    obj_l1: str = "ALL",
    obj_l2: str | None = None,
    itm_id: str = "ALL",
    prd_se: str = "M",
    save_as: str | None = None,
) -> pd.DataFrame:
    """표 ID와 기간으로 데이터를 받아 DataFrame으로 반환한다."""
    params = {
        "method": "getList",
        "apiKey": _api_key(),
        "format": "json",
        "jsonVD": "Y",
        "orgId": KOSIS_ORG_ID,
        "tblId": tbl_id,
        "itmId": itm_id,
        "objL1": obj_l1,
        "prdSe": prd_se,
        "startPrdDe": start,
        "endPrdDe": end,
    }
    if obj_l2:
        params["objL2"] = obj_l2
    resp = requests.get(BASE_URL, params=params, timeout=60)
    resp.raise_for_status()
    df = _to_frame(resp.json())
    if save_as:
        df.to_csv(DATA_RAW / save_as, index=False, encoding="utf-8-sig")
    return df


def fetch_url(url: str, save_as: str | None = None) -> pd.DataFrame:
    """KOSIS 'URL 생성'으로 받은 주소를 그대로 호출한다 (apiKey 자리는 자동 치환)."""
    url = url.replace("인증키없음", _api_key())
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    df = _to_frame(resp.json())
    if save_as:
        df.to_csv(DATA_RAW / save_as, index=False, encoding="utf-8-sig")
    return df
