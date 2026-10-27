"""Training table: ensemble features (+ deterministic features where the
archive has them) joined to PowderBench truth windows.

Rows are driven by the ensemble archive (GEFS from 2020, ECMWF ENS from
2024), so most training rows carry *only* ensemble features. That is exactly
the situation of non-featured network stations live (no Open-Meteo fetch for
them), and the deterministic multi-model features from late 2024 on teach
the model what the extra models add for featured stations.
"""

from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from . import features, store, truth
from .contract import climatology, stations

SH_LEAGUES = ("era5", "resorts")
HF_LEAGUES = ("stations", "observers", "alps")
KEYS = ["station_id", "round_date", "horizon_h"]


def season_of(d: pd.Series, league: str) -> pd.Series:
    d = pd.to_datetime(d)
    if league in SH_LEAGUES:
        return d.dt.year
    return d.dt.year.where(d.dt.month >= 8, d.dt.year - 1)


def add_ref(df: pd.DataFrame) -> pd.DataFrame:
    """ref_snow: the raw consensus every layer compares against: the median
    of the ensembles' medians and the deterministic consensus, whichever exist."""
    cols = [c for c in ("gefs_snow_q50", "ecens_snow_q50", "cons_slr") if c in df]
    df["ref_snow"] = df[cols].median(axis=1) if cols else np.nan
    return df


def det_rows(dly: pd.DataFrame, league: str, live_round: date | None = None) -> pd.DataFrame:
    """Deterministic (Open-Meteo multi-model) wide features, no static columns."""
    if dly is None or dly.empty:
        return pd.DataFrame(columns=KEYS)
    win = features.live_windows(dly, live_round) if live_round else features.archive_windows(dly)
    return features.wide(win) if len(win) else pd.DataFrame(columns=KEYS)


def assemble(ens: pd.DataFrame, det: pd.DataFrame, league: str) -> pd.DataFrame:
    """ens rows (one per station/round/horizon) + deterministic columns where
    present + station metadata and climatology + ref_snow."""
    df = ens.merge(det, on=KEYS, how="left") if len(det) else ens.copy()
    df = features.add_static(df, stations(league), climatology(league), league)
    return add_ref(df)


def training_table(league: str) -> pd.DataFrame:
    from .ens_backfill import load

    ens = load(league)
    if ens.empty:
        return pd.DataFrame()
    det = det_rows(store.load_daily(league), league)
    X = assemble(ens, det, league)
    if league == "era5":
        tw = truth.windows(truth.era5_daily(stations(league), min(X["round_date"]), max(X["round_date"])))
    elif league in HF_LEAGUES:
        tw = truth.windows(truth.hf_daily(league, begin=min(X["round_date"])))
    else:  # resort leagues: PowderBench's own resolved rounds are the archive
        tw = truth.resolved_rounds(league)
    df = X.merge(tw, on=KEYS, how="inner")
    df["league"] = league
    df["season"] = season_of(df["round_date"], league)
    df["featured"] = df["station_id"].map(stations(league)["featured"]).fillna(False).astype(int)
    return df


def feature_rows(dly: pd.DataFrame, league: str, live_round: date | None = None) -> pd.DataFrame:
    """Deterministic-only rows (the path when the ensembles are unavailable)."""
    det = det_rows(dly, league, live_round)
    if det.empty:
        return pd.DataFrame()
    return add_ref(features.add_static(det, stations(league), climatology(league), league))
