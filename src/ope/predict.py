"""Build one round's submission.

1. Ensemble features (GEFS 31 + ECMWF ENS 51 members) for *every* station
   in the round, from the 00Z run a forecast at this league's cutoff can use.
2. The 10-model deterministic Open-Meteo features for featured stations.
3. Tier 1 (the trained GBM) on the union; network rows carry only the
   ensemble features, as most training rows do. Tier 0 (the ensembles'
   own quantiles) fills any gap, so a file always goes out.
4. Online bias from our own resolved rounds, then stacking on the public
   baselines merged into this round.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from . import HORIZONS, NH_LEAGUES, OWN_BUNDLE_LEAGUES, PROXY_LEAGUE, QCOLS, ROOT
from .contract import Round, stations
from .dataset import KEYS, assemble, det_rows, feature_rows
from .ens_features import features_for_init, init_for_round
from .features import daily
from .models import fallback, gbm, online, stack
from .sources import dynamical
from .sources import openmeteo as om
from .store import MODELS

HISTORY = ROOT / "history"
COLS = ["station_id", "horizon_h", "snowfall_in", *QCOLS, "prob_6in"]
FEATURED_MINUTES = 15


def bundle_names(league: str) -> list[str]:
    """Preference order: the league's own bundle, then its proxy's."""
    names = [league] if league in OWN_BUNDLE_LEAGUES else []
    base = PROXY_LEAGUE.get(league, league)
    return names + (["nh"] if base in NH_LEAGUES else [])


def load_bundle(league: str) -> tuple[str | None, gbm.Bundle | None]:
    for n in bundle_names(league):
        p = MODELS / f"{n}.pkl"
        if p.exists():
            return n, gbm.Bundle.load(p)
    return None, None


@dataclass
class Result:
    df: pd.DataFrame  # the submission
    raw: pd.DataFrame  # per row: raw_in (model), model_in (after online bias), final, tier
    info: dict


def live_ensembles(r: Round, st: pd.DataFrame, info: dict) -> pd.DataFrame:
    """Both ensembles at every station; the init a cutoff-time forecast can
    use (or the newest earlier one, if publication runs late)."""
    frames = []
    for name in dynamical.DATASETS:
        if not dynamical.applies(name, r.league):
            continue
        want = init_for_round(r.round_date, r.league, name)
        try:
            inits = dynamical.available_inits(name)
            ok = inits[(inits <= want) & (inits.hour == want.hour)]
            if not len(ok):
                continue
            init = ok[-1]
            f = features_for_init(name, init, st, r.league, round_date=r.round_date)
            if f.empty:
                continue
            frames.append(f.set_index(KEYS))
            info[f"{name}_init"] = str(init)[:13]
            print(f"  {r.key}: {name} {str(init)[:13]}Z at {len(st)} stations", flush=True)
        except Exception as e:  # one ensemble missing must not sink the round
            info[f"{name}_error"] = f"{type(e).__name__}: {str(e)[:120]}"
            print(f"  {r.key}: {name} failed: {e}", flush=True)
    if not frames:
        return pd.DataFrame(columns=KEYS)
    return pd.concat(frames, axis=1).reset_index()


def live_deterministic(r: Round, st: pd.DataFrame, info: dict) -> pd.DataFrame:
    if st.empty:
        return pd.DataFrame()
    ledger = om.Ledger(deadline=time.time() + FEATURED_MINUTES * 60)
    used0 = ledger.used
    try:
        h = om.fetch_by_region(st, r.target_days[0], r.target_days[-1], live=True, ledger=ledger)
    except om.QuotaExhausted as e:
        info["openmeteo_error"] = str(e)[:120]
        return pd.DataFrame()
    info["openmeteo_weight"] = round(ledger.used - used0, 1)
    return daily(h)


def _tier1(X: pd.DataFrame, as_league: str, bundle: gbm.Bundle) -> pd.DataFrame:
    Xb = X.copy()
    Xb["league_code"] = NH_LEAGUES.index(as_league) if as_league in NH_LEAGUES else len(NH_LEAGUES)
    t1 = gbm.predict(bundle, Xb)
    t1["tier"] = "t1"
    has_ens = X.filter(like="_snow_q50").notna().any(axis=1).to_numpy()
    t1 = t1[has_ens]
    # beyond the training range a tree model can't extrapolate: lean on tier 0
    p99 = bundle.metrics.get("ref_snow_p99", {})
    lim = X["horizon_h"].map(lambda h: p99.get(str(int(h)), np.inf)).to_numpy()[has_ens]
    ext = X["ref_snow"].to_numpy()[has_ens] > lim
    if ext.any():
        t0 = fallback.predict_ens(X).set_index(["station_id", "horizon_h"])
        idx = pd.MultiIndex.from_frame(t1.loc[ext, ["station_id", "horizon_h"]])
        for c in (*QCOLS, "snowfall_in"):
            base = t0[c].reindex(idx).to_numpy()
            t1.loc[ext, c] = np.fmax(t1.loc[ext, c].to_numpy(), 0.5 * (t1.loc[ext, c].to_numpy() + base))
        t1.loc[ext, "tier"] = "t1x"
    return t1


def build(r: Round, network: bool = True, budget: float | None = None) -> Result:
    reg = stations(r.league)
    ids = [s for s in (r.stations if network else r.featured) if s in reg.index]
    feat_ids = [s for s in r.featured if s in reg.index]
    bname, bundle = load_bundle(r.league)
    info: dict = {"round": r.key, "bundle": bname}
    proxy = r.league if bname == r.league else PROXY_LEAGUE.get(r.league, r.league)

    ens = live_ensembles(r, reg.loc[ids], info)
    dly = live_deterministic(r, reg.loc[feat_ids], info)
    det = det_rows(dly, r.league, live_round=r.round_date)
    if len(ens):
        X = assemble(ens, det, r.league)
    else:  # both ensembles down: deterministic-only tier 0 for the featured stations
        X = feature_rows(dly, r.league, live_round=r.round_date)
    if X.empty:
        raise RuntimeError("no forecast inputs at all (ensembles and Open-Meteo both failed)")

    t0 = fallback.predict_ens(X)
    t0["tier"] = "t0"
    parts = [_tier1(X, proxy, bundle)] if bundle is not None and len(ens) else []
    pred = pd.concat([*parts, t0], ignore_index=True).drop_duplicates(["station_id", "horizon_h"], keep="first")
    pred["raw_in"] = pred["snowfall_in"]
    pred = online.apply(pred, r.league, r.round_date)
    pred["model_in"] = pred["snowfall_in"]
    pred, stack_info = stack.apply(pred, r.league, r.round_date)
    info["stack"] = stack_info

    df = sanitize(pred)
    raw = pred[["station_id", "horizon_h", "raw_in", "model_in", "snowfall_in", *QCOLS, "prob_6in", "tier"]]
    fe = set(feat_ids)
    info.update(
        rows=len(df),
        featured_coverage=round(df[df.station_id.isin(fe)].shape[0] / max(1, 3 * len(fe)), 3),
        tiers=raw["tier"].value_counts().to_dict(),
    )
    return Result(df=df, raw=raw, info=info)


def sanitize(pred: pd.DataFrame) -> pd.DataFrame:
    """Exactly the PowderBench schema: numeric, clipped, monotone quantiles,
    p50 == snowfall_in, prob_6in only on 24 h rows, no duplicates."""
    df = pred[["station_id", "horizon_h", "snowfall_in", *QCOLS, "prob_6in"]].copy()
    df = df[df["horizon_h"].isin(HORIZONS)].dropna(subset=["snowfall_in"])
    df = df.drop_duplicates(["station_id", "horizon_h"])
    q = df[list(QCOLS)].apply(pd.to_numeric, errors="coerce")
    q["p50"] = df["snowfall_in"]
    for c in QCOLS:
        q[c] = q[c].fillna(q["p50"])
    arr = np.sort(np.clip(q.to_numpy(dtype=float), 0, 200), axis=1)
    df[list(QCOLS)] = np.round(arr, 2)
    df["snowfall_in"] = df["p50"]
    # cumulative horizons can't shrink: enforce h24 <= h48 <= h72 per station
    df = df.sort_values(["station_id", "horizon_h"])
    for c in (*QCOLS, "snowfall_in"):
        df[c] = df.groupby("station_id")[c].cummax()
    p = pd.to_numeric(df["prob_6in"], errors="coerce").clip(0.001, 0.999).round(3)
    df["prob_6in"] = p.where(df["horizon_h"] == 24)
    return df.reset_index(drop=True)


def write(res: Result, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    res.df.to_csv(out, index=False)
    return out
