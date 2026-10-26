"""Ensemble forecasts from dynamical.org's open Zarr archives (CC BY 4.0).

- GEFS (NOAA): 31 members, 00Z runs since 2020-10, 0.25 deg, 3-hourly. Precip,
  2 m temperature, percent frozen precipitation, 2 m relative humidity.
- ECMWF IFS ENS: 51 members, 00Z runs since 2024-04, 0.25 deg, 3-hourly.
  Precip, 2 m temperature and dew point, 850 hPa temperature.

No API quota: the stores are sharded Zarr on object storage and only the
inner chunks around the requested stations are read. Every station of every
league (the full networks) is covered for the cost of reading a few tiles.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
import pandas as pd

BASE = "https://data.dynamical.org"


@dataclass(frozen=True)
class Dataset:
    name: str
    url: str
    variables: dict[str, str]  # zarr name -> short name
    first_init: str


DATASETS = {
    "gefs": Dataset(
        "gefs", f"{BASE}/noaa/gefs/forecast-35-day/latest.zarr",
        {"precipitation_surface": "p", "temperature_2m": "t2m",
         "percent_frozen_precipitation_surface": "pfz", "relative_humidity_2m": "rh"},
        "2020-10-01"),
    "ecens": Dataset(
        "ecens", f"{BASE}/ecmwf/ifs-ens/forecast-15-day-0-25-degree/latest.zarr",
        {"precipitation_surface": "p", "temperature_2m": "t2m",
         "dew_point_temperature_2m": "td", "temperature_850hpa": "t850"},
        "2024-04-01"),
}
STEP_S = 3 * 3600  # 3-hourly steps; precip is a mean rate over the step
MAX_LEAD_H = 132  # a D-2 00Z run to the end of local day D+2 anywhere


_open_cache: dict[str, object] = {}


def open_dataset(name: str):
    import xarray as xr

    if name not in _open_cache:
        _open_cache[name] = xr.open_zarr(DATASETS[name].url, decode_timedelta=True, chunks=None)
    return _open_cache[name]


def available_inits(name: str) -> pd.DatetimeIndex:
    return pd.DatetimeIndex(open_dataset(name).init_time.values)


def extract(name: str, init: pd.Timestamp, st: pd.DataFrame, retries: int = 5) -> pd.DataFrame:
    """One run at the stations' nearest grid points -> long frame:
    station_id, member, valid (UTC, end of the 3 h step), and the dataset's
    variables (p in mm per step; temperatures in C; pfz/rh in %)."""
    import xarray as xr

    ds = open_dataset(name)
    spec = DATASETS[name]
    n_lead = MAX_LEAD_H // 3 + 1
    lat = xr.DataArray(st["latitude"].to_numpy(), dims="pt")
    lon = xr.DataArray(((st["longitude"].to_numpy() + 180) % 360) - 180, dims="pt")
    sub = (ds[list(spec.variables)].sel(init_time=np.datetime64(init.tz_localize(None) if init.tzinfo else init))
           .isel(lead_time=slice(0, n_lead)).sel(latitude=lat, longitude=lon, method="nearest"))
    for attempt in range(retries):
        try:
            v = sub.load()
            break
        except Exception:  # flaky range reads: back off and retry
            if attempt == retries - 1:
                raise
            time.sleep(5 * (attempt + 1))
    lead = pd.to_timedelta(v["lead_time"].values)
    valid = pd.Timestamp(init).tz_localize(None) + lead
    members = v["ensemble_member"].values
    out = {}
    for zname, short in spec.variables.items():
        a = v[zname].transpose("pt", "ensemble_member", "lead_time").to_numpy().astype("float32")
        out[short] = a.reshape(-1)
    n_pt, n_mem, n_ld = len(st), len(members), len(lead)
    df = pd.DataFrame(out)
    df["station_id"] = np.repeat(st.index.to_numpy(), n_mem * n_ld)
    df["member"] = np.tile(np.repeat(members, n_ld), n_pt)
    df["valid"] = np.tile(valid.to_numpy(), n_pt * n_mem)
    df["p"] = df["p"] * STEP_S  # mean rate (kg m-2 s-1) -> mm over the 3 h step
    return df[df["valid"] > pd.Timestamp(init).tz_localize(None)]
