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
_Updated 2026-11-03 03:05 UTC from PowderBench leaderboards._

### era5 — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-climatology | 0.0 | 0.96 | 0.379 | 0.030 | 108 |
| 2 | baseline-zeros | -1.3 | 0.97 | 0.485 | 0.031 | 112 |
| 3 | baseline-gfs | -25.8 | 0.77 | – | – | 112 |
| 4 | baseline-openmeteo | -34.0 | 0.85 | – | – | 112 |
| 5 | baseline-persistence | -201.1 | 1.44 | – | – | 112 |
| None | southern-league-mogger | 51.7 | 0.38 | 0.152 | 0.000 | 1 |

### observers — **#None** of 17 (Powder Accuracy 48.8, 1 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-ukmo | 21.6 | 0.16 | – | – | 7 |
| 2 | baseline-consensus | 17.6 | 0.17 | – | – | 7 |
| 3 | baseline-icon | 16.1 | 0.17 | – | – | 7 |
| 4 | baseline-gem | 11.1 | 0.17 | – | – | 7 |
| 5 | baseline-zeros | 1.2 | 0.21 | 0.105 | 0.000 | 7 |
| 6 | baseline-climatology | 0.0 | 0.18 | 0.104 | 0.000 | 5 |
| None | **open-powder-ensemble** | 48.8 | 0.09 | 0.040 | 0.000 | 1 |

### resorts — **#None** of 17 (Powder Accuracy -5747.6, 3 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-icon | 18.5 | 0.17 | – | – | 9 |
| 2 | baseline-zeros | 3.2 | 4.41 | 2.205 | 0.129 | 110 |
| 3 | baseline-climatology | 0.0 | 4.51 | 2.045 | 0.127 | 106 |
| 4 | baseline-openmeteo | -74.3 | 3.79 | – | – | 110 |
| 5 | baseline-gfs | -78.8 | 3.68 | – | – | 110 |
| 6 | baseline-persistence | -115.4 | 4.04 | – | – | 110 |
| None | **open-powder-ensemble** | -5747.6 | 1.21 | 0.456 | 0.082 | 3 |

### stations — **#None** of 16 (Powder Accuracy 41.9, 4 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-wpc | 27.2 | 0.81 | 0.314 | 0.016 | 7 |
| 2 | open-powder-ml | 24.6 | 0.94 | 0.356 | 0.020 | 7 |
| 3 | baseline-consensus | 23.0 | 0.81 | – | – | 9 |
| 4 | house-blend | 21.4 | 0.94 | 0.460 | 0.032 | 7 |
| 5 | baseline-ukmo | 20.4 | 0.85 | – | – | 10 |
| 6 | baseline-ecmwf | 15.4 | 0.96 | – | – | 6 |
| None | **open-powder-ensemble** | 41.9 | 0.85 | 0.320 | 0.013 | 4 |

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
