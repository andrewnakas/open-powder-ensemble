"""Forecast archives from dynamical.org (all CC BY 4.0), read point-wise.

| key     | model                     | members | runs used        | archive from | grid            |
|---------|---------------------------|---------|------------------|--------------|-----------------|
| gefs    | NOAA GEFS                 | 31      | 00Z              | 2020-10      | 0.25 deg        |
| ecens   | ECMWF IFS ENS             | 51      | 00Z              | 2024-04      | 0.25 deg        |
| gfs     | NOAA GFS                  | 1       | 00Z              | 2021-05      | 0.25 deg        |
| hrrr    | NOAA HRRR (CONUS, 3 km)   | 1       | 12Z (48 h runs)  | 2018-07      | Lambert y/x     |
| aifs    | ECMWF AIFS (AI)           | 1       | 00Z              | 2024-04      | 0.25 deg        |
| aifsens | ECMWF AIFS ENS (AI)       | 51      | 00Z              | 2025-07      | 0.25 deg        |

The Zarr / Icechunk stores are sharded on object storage (the newer ones on
AWS Open Data buckets), and only the inner chunks around the requested
stations are read. No API quota.

Precipitation is a mean rate over the step ending at each lead, so per-step
amounts are rate x step length; step lengths come from the lead spacing
(GFS is hourly, then 3-hourly; HRRR hourly; the AI models 6-hourly).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

BASE = "https://data.dynamical.org"


@dataclass(frozen=True)
class Dataset:
    name: str
    variables: dict[str, str]  # store name -> short name
    first_init: str
    physics: str  # "frozen" (percent-frozen + 2 m T) | "upper" (wet-bulb + 850 hPa T)
    url: str | None = None  # plain Zarr
    icechunk: tuple[str, str] | None = None  # (bucket, prefix) on AWS us-west-2
    init_hour: int = 0
    max_lead_h: int = 132
    conus_only: bool = False
    leagues: tuple[str, ...] = field(default=())  # () = every league


DATASETS = {
    "gefs": Dataset(
        "gefs", {"precipitation_surface": "p", "temperature_2m": "t2m",
                 "percent_frozen_precipitation_surface": "pfz"},
        "2020-10-01", "frozen", url=f"{BASE}/noaa/gefs/forecast-35-day/latest.zarr"),
    "ecens": Dataset(
        "ecens", {"precipitation_surface": "p", "temperature_2m": "t2m",
                  "dew_point_temperature_2m": "td", "temperature_850hpa": "t850"},
        "2024-04-01", "upper", url=f"{BASE}/ecmwf/ifs-ens/forecast-15-day-0-25-degree/latest.zarr"),
    "gfs": Dataset(
        "gfs", {"precipitation_surface": "p", "temperature_2m": "t2m",
                "percent_frozen_precipitation_surface": "pfz"},
        "2021-05-01", "frozen", icechunk=("dynamical-noaa-gfs", "noaa-gfs-forecast/v0.2.7.icechunk")),
    "hrrr": Dataset(
        "hrrr", {"precipitation_surface": "p", "temperature_2m": "t2m",
                 "percent_frozen_precipitation_surface": "pfz", "snowfall_surface": "nsnow"},
        "2018-08-01", "frozen", icechunk=("dynamical-noaa-hrrr", "noaa-hrrr-forecast-48-hour/v0.1.0.icechunk"),
        init_hour=12, max_lead_h=48, conus_only=True, leagues=("stations", "observers", "resorts-na")),
    "aifs": Dataset(
        "aifs", {"precipitation_surface": "p", "temperature_2m": "t2m",
                 "dew_point_temperature_2m": "td", "temperature_850hpa": "t850"},
        "2024-04-01", "upper", icechunk=("dynamical-ecmwf-aifs-single", "ecmwf-aifs-single-forecast/v0.1.0.icechunk")),
    "aifsens": Dataset(
        "aifsens", {"precipitation_surface": "p", "temperature_2m": "t2m",
                    "dew_point_temperature_2m": "td", "temperature_850hpa": "t850"},
        "2025-07-01", "upper", icechunk=("dynamical-ecmwf-aifs-ens", "ecmwf-aifs-ens-forecast/v0.1.0.icechunk")),
}


def in_conus(lat, lon):
    lat, lon = np.asarray(lat), np.asarray(lon)
    return (lat >= 24.0) & (lat <= 50.0) & (lon >= -125.5) & (lon <= -66.0)


def applies(name: str, league: str) -> bool:
    spec = DATASETS[name]
    return not spec.leagues or league in spec.leagues


_open_cache: dict[str, object] = {}
_tree_cache: dict[str, object] = {}


def open_dataset(name: str):
    import xarray as xr

    if name not in _open_cache:
        spec = DATASETS[name]
        if spec.icechunk:
            import icechunk

            bucket, prefix = spec.icechunk
            st = icechunk.s3_storage(bucket=bucket, prefix=prefix, region="us-west-2", anonymous=True)
            store = icechunk.Repository.open(st).readonly_session("main").store
            _open_cache[name] = xr.open_zarr(store, consolidated=False, decode_timedelta=True, chunks=None)
        else:
            _open_cache[name] = xr.open_zarr(spec.url, decode_timedelta=True, chunks=None)
    return _open_cache[name]


def available_inits(name: str) -> pd.DatetimeIndex:
    return pd.DatetimeIndex(open_dataset(name).init_time.values)


def _nearest_yx(name: str, lat: np.ndarray, lon: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Projected grids (HRRR): nearest cell on the 2-D lat/lon coordinates."""
    from scipy.spatial import cKDTree

    ds = open_dataset(name)
    if name not in _tree_cache:
        la, lo = np.radians(ds["latitude"].values), np.radians(ds["longitude"].values)
        xyz = np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1).reshape(-1, 3)
        _tree_cache[name] = (cKDTree(xyz), ds["latitude"].shape)
    tree, shape = _tree_cache[name]
    la, lo = np.radians(lat), np.radians(lon)
    _, idx = tree.query(np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1))
    return np.unravel_index(idx, shape)


def extract(name: str, init: pd.Timestamp, st: pd.DataFrame, retries: int = 5) -> pd.DataFrame:
    """One run at the stations' nearest grid points -> long frame: station_id,
    member, valid (UTC, end of the step), dt_h (step length), and the
    dataset's variables (p in mm over the step; temperatures in C; pfz in %;
    nsnow = the model's own snowfall in mm of snow over the step)."""
    import xarray as xr

    ds = open_dataset(name)
    spec = DATASETS[name]
    if spec.conus_only:
        st = st[in_conus(st["latitude"], st["longitude"])]
    if st.empty:
        return pd.DataFrame()
    init = pd.Timestamp(init).tz_localize(None) if pd.Timestamp(init).tzinfo else pd.Timestamp(init)
    sub = ds[list(spec.variables)].sel(init_time=np.datetime64(init))
    lead_h = pd.to_timedelta(sub["lead_time"].values) / pd.Timedelta(hours=1)
    sub = sub.isel(lead_time=np.nonzero(lead_h <= spec.max_lead_h)[0])
    lat = st["latitude"].to_numpy()
    lon = ((st["longitude"].to_numpy() + 180) % 360) - 180
    if "x" in sub.dims:
        yi, xi = _nearest_yx(name, lat, lon)
        sub = sub.isel(y=xr.DataArray(yi, dims="pt"), x=xr.DataArray(xi, dims="pt"))
    else:
        sub = sub.sel(latitude=xr.DataArray(lat, dims="pt"), longitude=xr.DataArray(lon, dims="pt"), method="nearest")
    for attempt in range(retries):
        try:
            v = sub.load()
            break
        except Exception:  # flaky range reads: back off and retry
            if attempt == retries - 1:
                raise
            time.sleep(5 * (attempt + 1))
    lead = pd.to_timedelta(v["lead_time"].values)
    dt_h = np.diff(lead / pd.Timedelta(hours=1), prepend=0.0)
    members = v["ensemble_member"].values if "ensemble_member" in v.dims else np.array([0])
    n_pt, n_mem, n_ld = len(st), len(members), len(lead)
    out = {}
    for zname, short in spec.variables.items():
        a = v[zname]
        if "ensemble_member" not in a.dims:
            a = a.expand_dims(ensemble_member=members)
        out[short] = a.transpose("pt", "ensemble_member", "lead_time").to_numpy().astype("float32").reshape(-1)
    df = pd.DataFrame(out)
    df["station_id"] = np.repeat(st.index.to_numpy(), n_mem * n_ld)
    df["member"] = np.tile(np.repeat(members, n_ld), n_pt)
    df["valid"] = np.tile((init + lead).to_numpy(), n_pt * n_mem)
    df["dt_h"] = np.tile(dt_h, n_pt * n_mem)
    df["p"] = df["p"] * df["dt_h"] * 3600  # mean rate (kg m-2 s-1) -> mm over the step
    if "nsnow" in df:
        df["nsnow"] = df["nsnow"] * df["dt_h"] * 3600 * 1000  # m/s of snow -> mm over the step
    return df[df["dt_h"] > 0]
