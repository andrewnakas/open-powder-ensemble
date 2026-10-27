# Method

The targets, the scoring and the deterministic features are as in
[open-powder-ml](https://github.com/andrewnakas/open-powder-ml/blob/main/docs/METHOD.md). This
entry adds the following.

## Forecast archives (dynamical.org, CC BY 4.0)
- **Ensembles:** GEFS (31 members, 00Z, from 2020-10), ECMWF IFS ENS (51, from 2024-04) and
  ECMWF AIFS ENS (51, the AI ensemble, from 2025-07).
- **Single runs:** GFS (from 2021-05), ECMWF AIFS (from 2024-04) and HRRR.
- **HRRR:** the 3 km CONUS model, from 2018. It uses the 12Z D−1 runs; their 48 h reach covers
  local day D, so HRRR feeds the 24 h horizon only. It includes HRRR's own snowfall field.

Every archive is lead-correct: training rows use exactly the run a cutoff-time forecast could
have used. Deterministic runs contribute mean snow, liquid, frozen fraction and temperature
(their quantiles would say nothing).

## Ensemble features
For each round D, the forecast uses the 00Z run that a forecast made at the league's cutoff could
use:
- **Northern Hemisphere leagues:** D−1 00Z. dynamical.org publishes it well before 00Z D or
  21Z D−1.
- **Southern Hemisphere leagues** (cutoff 11Z D−1): D−2 00Z.

Training uses exactly the same rule, so there is no look-ahead.

Each member's 3-hourly output at the station's nearest grid point is turned into snow:
- **GEFS:** precipitation × the model's own percent-frozen precipitation × a snow-to-liquid ratio
  from 2 m temperature.
- **ECMWF ENS:** precipitation × a logistic rain/snow split on the **2 m wet-bulb temperature**
  (Stull 2011, from temperature and dew point) × a ratio from **850 hPa temperature**. The cloud
  layer, not the surface, sets crystal habit and density.

The 3-hour steps are summed into **station-local days** using each station's time zone (by step
midpoint), then into the cumulative windows D, D..D+1 and D..D+2.

Per ensemble and window, the features are:
- the members' mean, p10/p25/p50/p75/p90 and SD
- P(≥1″) and P(≥6″)
- the frozen fraction
- the precipitation-weighted temperature

## Model
LightGBM quantile models (p10…p90) and a P(≥6″) classifier are trained on the union of features:
- ensemble features, deterministic multi-model features where present, station metadata and
  PowderBench climatology
- a per-station bias feature, computed out-of-fold

Rows come from the ensemble archive: GEFS from 2020-10 and ECMWF ENS from 2024-04, sampled every
2nd day from November to April (June to September in the Southern Hemisphere).

So most rows carry only ensemble features. That is also the situation of non-featured network
stations live, so they stay in-distribution.

Calibration, the extrapolation guard, the promotion gate and the online bias layer are as in
open-powder-ml. The `ref_snow` reference is the median of the ensemble medians and the
deterministic consensus.

## Stacking on the public baselines
PowderBench's `baseline-*` files (NBM, HRRR, WPC percentiles, NDFD, model consensus, …) are merged
into each round hours before the cutoff, so later update passes can see them.

From our own resolved rounds, this layer picks the single baseline partner and blend weight that
cut historical MAE the most.
- It needs at least 8 rounds and at least 2% gain to switch on.
- It blends p50, and blends quantiles and P(≥6″) where the partner has them (WPC). Otherwise it
  rescales our quantiles.
- Other competitors' submissions are never used.

## Terrain
Every station gets static terrain features from the Copernicus GLO-30 DEM (30 m), computed by
`scripts/terrain.py` and stored in `data/terrain.parquet`. The method follows mountainweather/mtnwx.
- **Local terrain:** relief within 10 km, slope, aspect, and topographic position (TPI) at 500 m,
  2 km and 10 km.
- **Height above the model grid:** the station's height above the mean terrain of a ~3 km cell
  (HRRR) and of a 0.25° cell (GEFS/ECMWF/GFS). Coarse models report 2 m temperature at their
  smoothed orography, so this offset explains much of their warm, rainy bias on mountain stations.

DEM © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018, provided under COPERNICUS
by the European Union and ESA.
