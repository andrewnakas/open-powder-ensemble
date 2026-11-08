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
_Updated 2026-11-08 00:54 UTC from PowderBench leaderboards._

### alps — **#None** of 15 (Powder Accuracy 18.1, 2 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| None | open-powder-ml | 32.0 | 0.08 | 0.032 | 0.000 | 2 |
| None | baseline-ukmo | 31.2 | 0.08 | – | – | 2 |
| None | baseline-consensus | 31.2 | 0.08 | – | – | 2 |
| None | baseline-gem | 27.2 | 0.09 | – | – | 2 |
| None | baseline-openmeteo | 26.2 | 0.09 | – | – | 2 |
| None | baseline-arome | 26.1 | 0.09 | – | – | 2 |
| None | **open-powder-ensemble** | 18.1 | 0.10 | 0.035 | 0.000 | 2 |

### era5 — **#None** of 17 (Powder Accuracy 81.5, 3 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | open-powder-ml | 53.0 | 0.07 | 0.026 | 0.000 | 6 |
| 2 | house-gbm | 37.2 | 0.09 | 0.031 | 0.000 | 6 |
| 3 | house-analog | 36.2 | 0.09 | 0.036 | 0.000 | 7 |
| 4 | baseline-consensus | 18.7 | 0.11 | – | – | 9 |
| 5 | baseline-aifs | 14.5 | 0.11 | – | – | 9 |
| 6 | house-blend | 14.2 | 0.13 | 0.053 | 0.000 | 6 |
| None | **open-powder-ensemble** | 81.5 | 0.03 | 0.020 | 0.000 | 3 |

### observers — **#1** of 17 (Powder Accuracy 18.5, 6 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | **open-powder-ensemble** | 18.5 | 0.11 | 0.041 | 0.000 | 6 |
| 2 | baseline-icon | 14.0 | 0.14 | – | – | 12 |
| 3 | baseline-consensus | 11.2 | 0.14 | – | – | 12 |
| 4 | baseline-zeros | 5.2 | 0.17 | 0.085 | 0.000 | 12 |
| 5 | baseline-ukmo | 3.5 | 0.15 | – | – | 12 |
| 6 | baseline-climatology | 0.0 | 0.15 | 0.100 | 0.000 | 10 |

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

### resorts-na — **#None** of 17 (Powder Accuracy 7.8, 3 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| None | baseline-gfs | 18.1 | 1.09 | – | – | 3 |
| None | baseline-openmeteo | 18.1 | 1.09 | – | – | 3 |
| None | baseline-wpc | 13.9 | 1.22 | 0.532 | 0.064 | 3 |
| None | house-blend | 9.8 | 1.25 | 0.539 | 0.081 | 3 |
| None | baseline-consensus | 9.1 | 1.29 | – | – | 3 |
| None | **open-powder-ensemble** | 7.8 | 1.33 | 0.589 | 0.072 | 3 |

### stations — **#14** of 16 (Powder Accuracy -32.0, 9 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-wpc | 32.7 | 0.78 | 0.297 | 0.015 | 11 |
| 2 | baseline-consensus | 28.5 | 0.82 | – | – | 14 |
| 3 | house-blend | 26.8 | 0.90 | 0.414 | 0.028 | 12 |
| 4 | baseline-ukmo | 20.6 | 0.92 | – | – | 15 |
| 5 | baseline-ecmwf | 18.4 | 0.93 | – | – | 7 |
| 6 | baseline-icon | 16.0 | 0.98 | – | – | 15 |
| 14 | **open-powder-ensemble** | -32.0 | 1.74 | 0.600 | 0.022 | 9 |

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
- Finished units go to the `ens-store` release.

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
