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
_Updated 2026-11-28 03:30 UTC from PowderBench leaderboards._

### alps — **#15** of 16 (Powder Accuracy -8.6, 22 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | deep-powder | 49.8 | 2.29 | 0.785 | 0.081 | 7 |
| 2 | baseline-ukmo | 21.7 | 1.80 | – | – | 13 |
| 3 | baseline-consensus | 20.6 | 1.69 | – | – | 13 |
| 4 | baseline-openmeteo | 20.3 | 1.60 | – | – | 13 |
| 5 | baseline-icon | 19.3 | 1.62 | – | – | 13 |
| 6 | house-blend | 17.1 | 1.65 | 0.746 | 0.080 | 13 |
| 15 | **open-powder-ensemble** | -8.6 | 1.16 | 0.424 | 0.031 | 22 |

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

### observers — **#2** of 20 (Powder Accuracy 43.1, 26 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | deep-powder | 93.0 | 0.12 | 0.058 | 0.000 | 5 |
| 2 | **open-powder-ensemble** | 43.1 | 0.20 | 0.072 | 0.002 | 26 |
| 3 | baseline-consensus | 29.5 | 0.16 | – | – | 26 |
| 4 | baseline-icon | 24.6 | 0.19 | – | – | 26 |
| 5 | baseline-ukmo | 23.8 | 0.15 | – | – | 26 |
| 6 | baseline-zeros | 22.7 | 0.22 | 0.109 | 0.002 | 27 |

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

### resorts-na — **#8** of 18 (Powder Accuracy 7.8, 23 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-ecmwf | 28.3 | 1.23 | – | – | 10 |
| 2 | deep-powder | 27.3 | 1.74 | 0.693 | 0.075 | 7 |
| 3 | baseline-icon | 21.0 | 1.46 | – | – | 16 |
| 4 | baseline-aifs | 17.5 | 1.50 | – | – | 16 |
| 5 | baseline-wpc | 17.5 | 1.43 | 0.630 | 0.048 | 15 |
| 6 | baseline-consensus | 15.7 | 1.46 | – | – | 16 |
| 8 | **open-powder-ensemble** | 7.8 | 1.54 | 0.653 | 0.052 | 23 |

### stations — **#12** of 19 (Powder Accuracy 16.9, 29 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | deep-powder | 48.3 | 1.05 | 0.372 | 0.031 | 8 |
| 2 | house-analog | 36.3 | 1.05 | 0.383 | 0.023 | 16 |
| 3 | baseline-consensus | 35.3 | 0.86 | – | – | 31 |
| 4 | house-gbm | 33.9 | 0.97 | 0.368 | 0.019 | 16 |
| 5 | house-blend | 32.4 | 0.85 | 0.380 | 0.023 | 29 |
| 6 | baseline-ecmwf | 31.2 | 0.93 | – | – | 16 |
| 12 | **open-powder-ensemble** | 16.9 | 1.21 | 0.440 | 0.022 | 29 |

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
