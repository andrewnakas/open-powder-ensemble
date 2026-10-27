"""Resumable harvest of historical ensemble features for training.

A unit = (dataset, league, month). It holds the featured stations' ensemble
features for every 2nd 00Z run of the month (every run would read ~2x the
data from dynamical.org for little extra skill). Finished units are parquet
files in work/ens_store, synced to the `ens-store` release, and a run stops
cleanly at its time budget, so daily jobs simply continue where the last
stopped.
"""

from __future__ import annotations

import time
from datetime import date

import pandas as pd

from . import WORK, store
from .contract import stations
from .ens_features import features_for_init
from .sources.dynamical import DATASETS, applies

ENS_STORE = WORK / "ens_store"
NH_MONTHS = (11, 12, 1, 2, 3, 4)
SH_MONTHS = (6, 7, 8, 9)
EVERY_N_DAYS = 2


# Beyond the featured stations, a fixed random sample of each network's other
# stations with truth: ~3x the training rows, and the same kind of stations
# the full-network forecasts are made for.
NETWORK_SAMPLE = {"stations": 300, "observers": 300, "alps": 100}
NET = "-net"


def unit_name(ds: str, league: str, month: pd.Period) -> str:
    return f"ens__{ds}__{league}__{month}.parquet"


def unit_stations(league: str) -> pd.DataFrame:
    """league 'x' = featured stations; 'x-net' = the network sample."""
    base = league.removesuffix(NET)
    st = stations(base)
    if not league.endswith(NET):
        return st[st["featured"]]
    rest = st[~st["featured"]]
    return rest.sample(min(NETWORK_SAMPLE.get(base, 0), len(rest)), random_state=11).sort_index()


def units(leagues: list[str], end: date) -> list[tuple[str, str, pd.Period]]:
    out = []
    leagues = list(leagues) + [lg + NET for lg in leagues if lg in NETWORK_SAMPLE]
    for ds, spec in DATASETS.items():
        for lg in leagues:
            if not applies(ds, lg.removesuffix(NET)):
                continue
            months = SH_MONTHS if lg in ("era5", "resorts") else NH_MONTHS
            # resort leagues only have truth since PowderBench's rounds began
            first = "2026-06-01" if lg in ("resorts", "resorts-na") else spec.first_init
            for m in pd.period_range(max(first, spec.first_init), end, freq="M"):
                if m.month in months and m.end_time.date() <= end:
                    out.append((ds, lg, m))
    # winter core first, newest season first
    core = {1: 0, 2: 0, 12: 0, 7: 0, 8: 0, 3: 1, 11: 1, 6: 1, 9: 1, 4: 2}
    # featured first, then the network samples
    return sorted(out, key=lambda u: (u[1].endswith(NET), core.get(u[2].month, 3), -u[2].year, u[0], u[1]))


def harvest_unit(ds: str, league: str, month: pd.Period, deadline: float) -> pd.DataFrame | None:
    st = unit_stations(league)
    league = league.removesuffix(NET)
    hour = pd.Timedelta(hours=DATASETS[ds].init_hour)
    inits = pd.date_range(month.start_time, month.end_time.normalize(), freq=f"{EVERY_N_DAYS}D") + hour
    frames = []
    for init in inits:
        if time.time() > deadline:
            return None  # unfinished: redo next run (units are atomic)
        try:
            frames.append(features_for_init(ds, init, st, league))
        except KeyError:  # run missing from the archive
            continue
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def run(leagues: list[str], minutes: float = 300, end: date | None = None,
        datasets: list[str] | None = None) -> dict:
    end = end or (pd.Timestamp.utcnow() - pd.Timedelta(days=5)).date()
    deadline = time.time() + minutes * 60
    have = {p.name for p in ENS_STORE.glob("*.parquet")} | store.remote_assets("ens-store")
    todo = [u for u in units(leagues, end) if unit_name(*u) not in have and (not datasets or u[0] in datasets)]
    print(f"ens backfill: {len(todo)} units to go, {minutes:.0f} min budget", flush=True)
    done = []
    for ds, lg, m in todo:
        t0 = time.time()
        df = harvest_unit(ds, lg, m, deadline)
        if df is None:
            print("  time budget reached", flush=True)
            break
        p = ENS_STORE / unit_name(ds, lg, m)
        p.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(p, index=False)
        done.append(p)
        print(f"  {p.name}: {len(df)} rows in {time.time() - t0:.0f}s", flush=True)
        if len(done) % 5 == 0:  # don't lose work if the job dies
            store.push("ens-store", done[-5:])
    store.push("ens-store", done[-(len(done) % 5 or 5):] if done else [])
    return {"done": len(done), "remaining": len(todo) - len(done)}


def load(league: str) -> pd.DataFrame:
    """Every dataset's harvested features for a league, joined on the round keys."""
    keys = ["station_id", "round_date", "horizon_h"]
    out = None
    for ds in DATASETS:
        files = (sorted(ENS_STORE.glob(f"ens__{ds}__{league}__*.parquet"))
                 + sorted(ENS_STORE.glob(f"ens__{ds}__{league}{NET}__*.parquet")))
        if not files:
            continue
        f = pd.concat([pd.read_parquet(x) for x in files], ignore_index=True)
        f["round_date"] = pd.to_datetime(f["round_date"]).dt.date
        f = f.drop_duplicates(keys)
        out = f if out is None else out.merge(f, on=keys, how="outer")
    return out if out is not None else pd.DataFrame(columns=keys)
