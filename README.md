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
_Updated 2026-11-07 01:17 UTC from PowderBench leaderboards._

### alps — **#None** of 15 (Powder Accuracy -23.0, 1 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| None | baseline-gem | 2.4 | 0.12 | – | – | 1 |
| None | open-powder-ml | 0.7 | 0.12 | 0.042 | 0.000 | 1 |
| None | baseline-ukmo | 0.1 | 0.12 | – | – | 1 |
| None | baseline-climatology | 0.0 | 0.12 | 0.108 | 0.001 | 1 |
| None | baseline-consensus | -2.0 | 0.13 | – | – | 1 |
| None | baseline-arome | -10.1 | 0.14 | – | – | 1 |
| None | **open-powder-ensemble** | -23.0 | 0.15 | 0.047 | 0.000 | 1 |

### era5 — **#None** of 17 (Powder Accuracy 78.7, 1 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | house-analog | 38.8 | 0.07 | 0.028 | 0.000 | 5 |
| 2 | baseline-consensus | 27.2 | 0.08 | – | – | 7 |
| 3 | baseline-aifs | 13.8 | 0.10 | – | – | 7 |
| 4 | baseline-icon | 6.7 | 0.11 | – | – | 7 |
| 5 | baseline-ecmwf | 5.4 | 0.11 | – | – | 7 |
| 6 | baseline-climatology | 0.0 | 0.94 | 0.371 | 0.029 | 111 |
| None | **open-powder-ensemble** | 78.7 | 0.03 | 0.020 | 0.000 | 1 |

### observers — **#None** of 17 (Powder Accuracy 25.6, 4 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | open-powder-ml | 25.1 | 0.12 | 0.049 | 0.000 | 7 |
| 2 | baseline-icon | 14.8 | 0.14 | – | – | 10 |
| 3 | baseline-consensus | 7.5 | 0.14 | – | – | 10 |
| 4 | baseline-zeros | 5.5 | 0.17 | 0.085 | 0.000 | 10 |
| 5 | baseline-ukmo | 4.9 | 0.14 | – | – | 10 |
| 6 | baseline-wpc | 4.4 | 0.12 | 0.049 | 0.000 | 7 |
| None | **open-powder-ensemble** | 25.6 | 0.07 | 0.029 | 0.000 | 4 |

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

### resorts-na — **#None** of 17 (Powder Accuracy 27.1, 1 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| None | baseline-gfs | 65.7 | 0.71 | – | – | 1 |
| None | baseline-openmeteo | 65.7 | 0.71 | – | – | 1 |
| None | house-blend | 45.5 | 1.12 | 0.469 | 0.144 | 1 |
| None | baseline-nbm | 39.7 | 1.24 | – | – | 1 |
| None | baseline-wpc | 39.6 | 1.25 | 0.529 | 0.111 | 1 |
| None | baseline-ukmo | 36.9 | 1.30 | – | – | 1 |
| None | **open-powder-ensemble** | 27.1 | 1.50 | 0.640 | 0.120 | 1 |

### stations — **#13** of 16 (Powder Accuracy -26.7, 7 rounds)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-wpc | 32.0 | 0.86 | 0.331 | 0.017 | 9 |
| 2 | baseline-consensus | 25.8 | 0.90 | – | – | 12 |
| 3 | house-blend | 25.1 | 0.99 | 0.464 | 0.031 | 10 |
| 4 | baseline-ukmo | 19.2 | 0.99 | – | – | 13 |
| 5 | baseline-ecmwf | 18.4 | 0.93 | – | – | 7 |
| 6 | baseline-icon | 13.3 | 1.06 | – | – | 13 |
| 13 | **open-powder-ensemble** | -26.7 | 1.96 | 0.647 | 0.026 | 7 |

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
