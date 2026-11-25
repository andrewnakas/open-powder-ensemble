# open-powder-ensemble

An open-source machine-learning **research entry** in [PowderBench](https://powderbench.com), the
live mountain-snowfall benchmark. Every day, on GitHub Actions only, it forecasts every open round
of every in-season league for the **full station networks**, and submits through the same public
pull-request contract as every other player.

Research entries are declared in PowderBench's
[RULES.md](https://github.com/andrewnakas/powderbench/blob/main/docs/RULES.md). They:
- are maintainer-run and open-source
- follow the same cutoff and rules as everyone else
- never use other competitors' submissions

Its sibling [open-powder-ml](https://github.com/andrewnakas/open-powder-ml) is the deterministic
baseline this entry builds on.

## Standing

<!-- scoreboard:start -->
_Updated 2026-11-25 05:32 UTC from PowderBench leaderboards._

### alps — **#14** of 16 (Powder Accuracy -17.4, 19 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-ukmo | 19.5 | 1.24 | – | – | 10 |
| 2 | baseline-consensus | 18.3 | 1.12 | – | – | 10 |
| 3 | baseline-openmeteo | 17.9 | 1.03 | – | – | 10 |
| 4 | baseline-icon | 17.0 | 1.04 | – | – | 10 |
| 5 | house-blend | 13.6 | 1.10 | 0.491 | 0.038 | 10 |
| 6 | baseline-arome | 8.3 | 1.37 | – | – | 10 |
| 14 | **open-powder-ensemble** | -17.4 | 0.93 | 0.340 | 0.019 | 19 |

### era5 — **#None** of 17 (Powder Accuracy 48.8, 4 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | open-powder-ml | 29.9 | 0.06 | 0.023 | 0.000 | 7 |
| 2 | house-analog | 28.2 | 0.08 | 0.032 | 0.000 | 8 |
| 3 | house-gbm | 18.2 | 0.08 | 0.027 | 0.000 | 7 |
| 4 | baseline-icon | 5.3 | 0.11 | – | – | 10 |
| 5 | baseline-ecmwf | 0.6 | 0.13 | – | – | 9 |
| 6 | baseline-climatology | 0.0 | 0.92 | 0.362 | 0.029 | 114 |
| None | **open-powder-ensemble** | 48.8 | 0.03 | 0.016 | 0.000 | 4 |

### observers — **#1** of 20 (Powder Accuracy 38.0, 23 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | **open-powder-ensemble** | 38.0 | 0.18 | 0.069 | 0.002 | 23 |
| 2 | baseline-consensus | 29.5 | 0.16 | – | – | 26 |
| 3 | baseline-icon | 24.6 | 0.19 | – | – | 26 |
| 4 | baseline-ukmo | 23.8 | 0.15 | – | – | 26 |
| 5 | baseline-zeros | 22.7 | 0.22 | 0.109 | 0.002 | 27 |
| 6 | house-blend | 12.5 | 0.23 | 0.111 | 0.003 | 24 |

### resorts — **#None** of 17 (Powder Accuracy -5240.6, 4 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-icon | 23.4 | 0.15 | – | – | 10 |
| 2 | baseline-zeros | 4.1 | 4.37 | 2.185 | 0.127 | 111 |
| 3 | baseline-climatology | 0.0 | 4.47 | 2.027 | 0.126 | 107 |
| 4 | baseline-openmeteo | -80.2 | 3.76 | – | – | 111 |
| 5 | baseline-gfs | -82.2 | 3.65 | – | – | 111 |
| 6 | baseline-persistence | -113.5 | 4.00 | – | – | 111 |
| None | **open-powder-ensemble** | -5240.6 | 1.09 | 0.398 | 0.061 | 4 |

### resorts-na — **#7** of 18 (Powder Accuracy 5.8, 20 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-ecmwf | 28.9 | 1.25 | – | – | 9 |
| 2 | baseline-icon | 21.7 | 1.49 | – | – | 14 |
| 3 | baseline-wpc | 19.4 | 1.41 | 0.627 | 0.043 | 14 |
| 4 | baseline-aifs | 17.9 | 1.54 | – | – | 14 |
| 5 | baseline-zeros | 16.5 | 1.74 | 0.870 | 0.059 | 15 |
| 6 | baseline-consensus | 15.0 | 1.50 | – | – | 14 |
| 7 | **open-powder-ensemble** | 5.8 | 1.59 | 0.683 | 0.047 | 20 |

### stations — **#14** of 19 (Powder Accuracy 15.8, 26 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | deep-powder | 51.3 | 1.40 | 0.489 | 0.046 | 5 |
| 2 | house-gbm | 41.7 | 1.01 | 0.390 | 0.023 | 13 |
| 3 | house-analog | 41.4 | 1.14 | 0.418 | 0.026 | 13 |
| 4 | baseline-consensus | 37.7 | 0.88 | – | – | 28 |
| 5 | house-blend | 35.9 | 0.86 | 0.387 | 0.025 | 26 |
| 6 | baseline-wpc | 33.9 | 0.82 | 0.321 | 0.015 | 23 |
| 14 | **open-powder-ensemble** | 15.8 | 1.29 | 0.468 | 0.024 | 26 |

<!-- scoreboard:end -->

## What's better than open-powder-ml

| | open-powder-ml | **open-powder-ensemble** |
|---|---|---|
| Inputs | 10 deterministic NWP models (Open-Meteo) | the same, **plus six lead-correct archives from [dynamical.org](https://dynamical.org)**: GEFS (31 members, 2020–), ECMWF ENS (51, 2024–), GFS (2021–), **HRRR 3 km with its own snowfall** (2018–), ECMWF **AIFS** (AI, 2024–) and **AIFS ENS** (51, 2025–) |
| Network stations | 2 models, quota-limited, partial | ensembles at **every** station (no API quota) |
| Snow physics | 2 m temperature rain/snow split and snow ratio | GEFS percent-frozen; **wet-bulb** rain/snow split and **850 hPa** snow ratio for ECMWF |
| Uncertainty | quantile GBM on model spread | quantile GBM on **82-member** predictive distributions, P(≥6″) from members |
| Training history | Open-Meteo archive from late 2024 | GEFS from **2020** (6 winters) + ECMWF ENS from 2024 |
| Post-processing | online bias | online bias + **stacking on the public baselines**: NBM, WPC percentiles, NDFD, consensus |

See [docs/METHOD.md](docs/METHOD.md).

## How it runs

The submission machinery is the same as open-powder-ml.

**`forecast.yml` (keeper):** a self-chaining job that loops for about 5.5 h.
- It submits a round as soon as it opens, updates it on newer 00Z/12Z cycles, and resubmits
  anything that never merged.
- It never acts within 45 min of a cutoff.
- It only competes in a league once a trained model exists for it, because raw ensembles are not
  worth a season score.

**`backfill.yml`:** harvests the ensemble archive.
- It runs one parallel job per league, time-boxed and resumable.
- Finished units go to the `ens-store` releases: the original one plus one per year (`ens-store-2026`, ...), because GitHub caps a release at 1000 files.

**`train.yml`:** retrains daily.
- It trains on the ensemble archive plus open-powder-ml's public deterministic feature store, with
  PowderBench truth.
- It promotes a model only through the backtest gate, into the `models` release.

**`watchdog.yml`** and **`scoreboard.yml`** work as in open-powder-ml.

## Local use

```bash
scripts/checkout_powderbench.sh
pip install -e '.[dev]' ./work/powderbench
ope rounds
ope run --dry-run --force -l stations     # full network: ensembles + featured multi-model
ope backfill -l alps --minutes 20         # harvest ensemble archive units
ope train --bundle nh --no-promote
```

## Data and licences
- Ensemble data: dynamical.org Zarr archives of NOAA GEFS and ECMWF IFS ENS, CC BY 4.0.
- Deterministic models: [Open-Meteo](https://open-meteo.com), CC BY 4.0.
- Truth: PowderBench and its sources.
- Code: MIT.
