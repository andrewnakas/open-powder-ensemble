"""Tier 0: the always-available floor (no training needed).

Point = median across models of each model's snow (the mean of its own
snowfall and our temperature-based snow-physics estimate). Quantiles = the
spread across models, widened because a raw multi-model spread is
overconfident. P(>= 6") = a smoothed share of models over 6".
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .. import QCOLS

WIDEN = {"p10": 0.55, "p25": 0.8, "p50": 1.0, "p75": 1.2, "p90": 1.5}


def per_model(W: pd.DataFrame) -> pd.DataFrame:
    models = sorted({c.split("__", 1)[1] for c in W.columns if c.startswith("slr__")})
    vals = {}
    for m in models:
        s, k = W.get(f"slr__{m}"), W.get(f"snow__{m}")
        vals[m] = pd.concat([s, k], axis=1).mean(axis=1) if k is not None else s
    return pd.DataFrame(vals, index=W.index)


def predict(W: pd.DataFrame) -> pd.DataFrame:
    v = per_model(W)
    arr = v.to_numpy(dtype=float)
    ok = np.isfinite(arr).sum(axis=1) > 0
    q = np.full((len(W), 5), np.nan)
    if ok.any():
        q[ok] = np.nanpercentile(arr[ok], [10, 25, 50, 75, 90], axis=1).T
    out = pd.DataFrame(q, columns=list(QCOLS), index=W.index)
    for c in QCOLS:
        out[c] = out[c] * WIDEN[c]
    out = pd.DataFrame(np.sort(out.clip(0, 200).to_numpy(), axis=1), columns=list(QCOLS), index=W.index)
    out["snowfall_in"] = out["p50"]
    n = np.isfinite(arr).sum(axis=1)
    over = (np.nan_to_num(arr, nan=-1) >= 6).sum(axis=1)
    out["prob_6in"] = (over + 0.2) / (n + 1.0)
    keys = W[["station_id", "round_date", "horizon_h"]]
    return pd.concat([keys, out], axis=1)[ok]


ENS_WIDEN = {"p10": 0.8, "p25": 0.92, "p50": 1.0, "p75": 1.08, "p90": 1.2}


def predict_ens(X: pd.DataFrame) -> pd.DataFrame:
    """Tier 0 from the ensembles: the average of GEFS's and ECMWF ENS's member
    quantiles (lightly widened; raw ensembles are underdispersive), P(>=6")
    from the members. Rows without any ensemble data fall back to `predict`."""
    q = {}
    for c, lvl in zip(QCOLS, (10, 25, 50, 75, 90)):
        cols = [f"{d}_snow_q{lvl}" for d in ("gefs", "ecens") if f"{d}_snow_q{lvl}" in X]
        q[c] = X[cols].mean(axis=1) * ENS_WIDEN[c] if cols else pd.Series(np.nan, index=X.index)
    out = pd.DataFrame(q, index=X.index)
    ok = out["p50"].notna().to_numpy()
    arr = np.sort(out.clip(0, 200).to_numpy(), axis=1)
    out = pd.DataFrame(arr, columns=list(QCOLS), index=X.index)
    out["snowfall_in"] = out["p50"]
    pcols = [f"{d}_p_ge6" for d in ("gefs", "ecens") if f"{d}_p_ge6" in X]
    out["prob_6in"] = (X[pcols].mean(axis=1) * 0.9 + 0.01) if pcols else np.nan
    res = pd.concat([X[["station_id", "round_date", "horizon_h"]], out], axis=1)[ok]
    if (~ok).any() and any(c.startswith("slr__") for c in X.columns):
        res = pd.concat([res, predict(X[~ok])], ignore_index=True)
    return res
