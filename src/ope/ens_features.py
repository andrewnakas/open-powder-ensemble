"""Ensemble members -> station-local daily snow -> per-round ensemble features.

Snow physics per member (the upper-air part of the edge):
- GEFS: the model's own percent-frozen precipitation (falls back to a 2 m
  temperature split) x a 2 m temperature snow-to-liquid ratio.
- ECMWF ENS: rain/snow split on the 2 m wet-bulb temperature (from 2 m
  temperature + dew point), snow-to-liquid ratio from 850 hPa temperature
  (the cloud layer sets crystal habit and density, not the surface).

For each round D and horizon h the members' cumulative snow over local days
D..D+h/24-1 gives an empirical predictive distribution: its mean, quantiles,
exceedance probabilities, plus frozen fraction and temperature summaries.
"""

from __future__ import annotations

from datetime import date
from functools import cache

import numpy as np
import pandas as pd

from . import HORIZONS

MM_PER_IN = 25.4
QS = (0.1, 0.25, 0.5, 0.75, 0.9)


@cache
def _tz(lat: float, lon: float) -> str:
    from timezonefinder import TimezoneFinder

    return TimezoneFinder().timezone_at(lat=lat, lng=lon) or "UTC"


def station_tz(st: pd.DataFrame) -> pd.Series:
    return pd.Series([_tz(round(a, 3), round(b, 3)) for a, b in zip(st.latitude, st.longitude)], index=st.index)


def wet_bulb(t: np.ndarray, td: np.ndarray) -> np.ndarray:
    """Stull (2011) wet-bulb from temperature and dew point (C)."""
    es = lambda x: np.exp(17.625 * x / (243.04 + x))  # noqa: E731
    rh = np.clip(100 * es(td) / es(t), 1, 100)
    return (t * np.arctan(0.151977 * np.sqrt(rh + 8.313659)) + np.arctan(t + rh) - np.arctan(rh - 1.676331)
            + 0.00391838 * rh ** 1.5 * np.arctan(0.023101 * rh) - 4.686035)


def slr_2m(t: np.ndarray) -> np.ndarray:
    return np.clip(10.0 - 0.8 * t, 7.0, 20.0)


def slr_850(t850: np.ndarray) -> np.ndarray:
    return np.clip(10.0 + 0.8 * (-t850 - 5.0), 7.0, 22.0)


def member_snow(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Adds liquid (mm), frozen fraction, snow depth (mm) and the temperature
    that drives the ratio, per step (`dt_h` hours long)."""
    from .sources.dynamical import DATASETS

    p = df["p"].fillna(0.0).clip(lower=0).to_numpy()
    t2 = df["t2m"].to_numpy()
    if DATASETS[name].physics == "frozen":
        fz = df["pfz"].to_numpy() / 100.0
        fz = np.where(np.isfinite(fz), fz, 1.0 / (1.0 + np.exp((t2 - 1.0) / 0.5)))
        ratio, tdrv = slr_2m(np.nan_to_num(t2)), t2
    else:
        tw = wet_bulb(t2, df["td"].to_numpy())
        fz = 1.0 / (1.0 + np.exp((tw - 0.5) / 0.4))
        t850 = df["t850"].to_numpy()
        ratio, tdrv = slr_850(np.nan_to_num(t850)), t850
    fz = np.clip(np.nan_to_num(fz), 0, 1)
    out = df[["station_id", "member", "valid", "dt_h"]].copy()
    out["liq"], out["frz"], out["snow"], out["tdrv"] = p, p * fz, p * fz * ratio, np.nan_to_num(tdrv) * p
    # the model's own snowfall (HRRR), mm of snow
    out["nsnow"] = df["nsnow"].clip(lower=0).to_numpy() if "nsnow" in df else np.nan
    return out


def local_days(steps: pd.DataFrame, tz: pd.Series) -> pd.DataFrame:
    """Sum steps into station-local calendar days (by step midpoint); keep
    days the run covers completely (>= 23 h of steps)."""
    mid = pd.to_datetime(steps["valid"]) - pd.to_timedelta(steps["dt_h"] / 2, unit="h")
    dates = np.empty(len(steps), dtype=object)
    for zone, idx in steps.groupby(steps["station_id"].map(tz)).groups.items():
        dates[steps.index.get_indexer(idx)] = mid.loc[idx].dt.tz_localize("UTC").dt.tz_convert(zone).dt.date.to_numpy()
    steps = steps.assign(date=dates)
    g = steps.groupby(["station_id", "member", "date"], sort=False)
    d = g[["liq", "frz", "snow", "tdrv"]].sum()
    d["nsnow"] = g["nsnow"].sum(min_count=1)
    d["hrs"] = g["dt_h"].sum()
    return d[d["hrs"] >= 23].drop(columns="hrs").reset_index()


def round_features(days: pd.DataFrame, round_of: pd.Series, prefix: str) -> pd.DataFrame:
    """days: per station/member/local date; round_of: station_id -> round D.
    -> one row per (station_id, round_date, horizon_h) with `prefix`_ features."""
    days = days.copy()
    days["round_date"] = days["station_id"].map(round_of)
    days["i"] = (pd.to_datetime(days["date"]) - pd.to_datetime(days["round_date"])).dt.days
    rows = []
    for h in HORIZONS:
        n = h // 24
        w = days[(days["i"] >= 0) & (days["i"] < n)]
        g = w.groupby(["station_id", "round_date", "member"])
        m = g[["liq", "frz", "snow", "tdrv"]].sum()
        m["nsnow"] = g["nsnow"].sum(min_count=n)
        m = m[g.size() == n]  # every day of the window present
        m["snow_in"] = m["snow"] / MM_PER_IN
        m["liq_in"] = m["liq"] / MM_PER_IN
        s = m.groupby(level=["station_id", "round_date"])
        f = pd.DataFrame({
            "snow_mean": s["snow_in"].mean(),
            **{f"snow_q{int(q * 100)}": s["snow_in"].quantile(q) for q in QS},
            "snow_sd": s["snow_in"].std(),
            "liq_mean": s["liq_in"].mean(),
            "p_ge1": s["snow_in"].apply(lambda x: (x >= 1).mean()),
            "p_ge6": s["snow_in"].apply(lambda x: (x >= 6).mean()),
            "frz_frac": s["frz"].sum() / s["liq"].sum().clip(lower=0.1),
            "t_wet": s["tdrv"].sum() / s["liq"].sum().clip(lower=0.1),
            "n_mem": s.size(),
            "native_snow": s["nsnow"].mean() / MM_PER_IN,
        })
        if f["native_snow"].isna().all():
            f = f.drop(columns="native_snow")
        if f["n_mem"].max() == 1:  # deterministic run: quantiles and spreads say nothing
            f = f[["snow_mean", "liq_mean", "frz_frac", "t_wet", *(["native_snow"] if "native_snow" in f else [])]]
        f.columns = [f"{prefix}_{c}" for c in f.columns]
        f["horizon_h"] = h
        rows.append(f.reset_index())
    out = pd.concat(rows, ignore_index=True)
    out["round_date"] = pd.to_datetime(out["round_date"]).dt.date
    return out


DATA_MARGIN_H = 2.0  # the run must be published this long before the cutoff


def init_for_round(round_date: date, league: str, name: str = "gefs") -> pd.Timestamp:
    """The freshest run of `name` that a forecast made at this league's cutoff
    can use: published (init + the dataset's conservative delay) at least
    DATA_MARGIN_H hours before the cutoff. Training and live use this same
    rule, so features always have the lead time they will have live."""
    from . import use_pb_data

    use_pb_data()
    from powderbench.leagues import get_league

    from .sources.dynamical import DATASETS

    spec = DATASETS[name]
    cutoff = pd.Timestamp(get_league(league).cutoff_utc(round_date)).tz_localize(None)
    latest = cutoff - pd.Timedelta(hours=DATA_MARGIN_H + spec.latency_h)
    day = latest.normalize()
    for back in range(0, 3):
        for h in sorted(spec.init_hours, reverse=True):
            t = day - pd.Timedelta(days=back) + pd.Timedelta(hours=h)
            if t <= latest:
                return t
    return day - pd.Timedelta(days=3)


def features_for_init(name: str, init: pd.Timestamp, st: pd.DataFrame, league: str,
                      round_date: date | None = None) -> pd.DataFrame:
    """All stations of one league for one run. round_date defaults to the
    round this init serves at the league's cutoff; pass it explicitly when an
    older run stands in for a late one (the windows must be the round's days)."""
    from .sources.dynamical import extract

    raw = extract(name, init, st)
    if raw.empty:
        return pd.DataFrame()
    steps = member_snow(raw, name)
    days = local_days(steps.reset_index(drop=True), station_tz(st))
    if round_date is None:
        raise ValueError("round_date is required (the run-to-round mapping depends on the league's cutoff)")
    return round_features(days, pd.Series(round_date, index=st.index), name)
