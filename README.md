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
_Updated 2026-11-01 00:30 UTC from PowderBench leaderboards._

### era5 — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-climatology | 0.0 | 0.97 | 0.382 | 0.030 | 107 |
| 2 | baseline-zeros | -1.2 | 0.99 | 0.494 | 0.032 | 110 |
| 3 | baseline-gfs | -25.3 | 0.79 | – | – | 110 |
| 4 | baseline-openmeteo | -33.8 | 0.86 | – | – | 110 |
| 5 | baseline-persistence | -204.7 | 1.47 | – | – | 110 |
| None | southern-league-mogger | 51.7 | 0.38 | 0.152 | 0.000 | 1 |

### observers — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-gem | 17.7 | 0.18 | – | – | 5 |
| 2 | baseline-ukmo | 16.6 | 0.19 | – | – | 5 |
| 3 | baseline-consensus | 16.6 | 0.19 | – | – | 5 |
| 4 | baseline-icon | 16.5 | 0.19 | – | – | 5 |
| 5 | baseline-gfs | 10.2 | 0.20 | – | – | 5 |
| 6 | baseline-zeros | 0.8 | 0.24 | 0.120 | 0.000 | 5 |

### resorts — **#None** of 17 (Powder Accuracy -1173.8, 1 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-icon | 1.8 | 0.21 | – | – | 7 |
| 2 | baseline-zeros | 1.5 | 4.49 | 2.245 | 0.131 | 108 |
| 3 | baseline-climatology | 0.0 | 4.60 | 2.084 | 0.130 | 104 |
| 4 | baseline-openmeteo | -12.1 | 3.85 | – | – | 108 |
| 5 | baseline-ecmwf | -16.2 | 0.32 | – | – | 5 |
| 6 | baseline-gfs | -16.9 | 3.74 | – | – | 108 |
| None | **open-powder-ensemble** | -1173.8 | 0.27 | 0.215 | 0.052 | 1 |

### stations — **#None** of 16 (Powder Accuracy 50.4, 2 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | open-powder-ml | 34.0 | 0.72 | 0.281 | 0.025 | 5 |
| 2 | baseline-wpc | 30.0 | 0.76 | 0.291 | 0.023 | 5 |
| 3 | baseline-consensus | 24.4 | 0.70 | – | – | 7 |
| 4 | house-blend | 21.2 | 0.86 | 0.447 | 0.041 | 5 |
| 5 | baseline-ukmo | 20.6 | 0.77 | – | – | 8 |
| 6 | baseline-ecmwf | 15.5 | 0.84 | – | – | 5 |
| None | **open-powder-ensemble** | 50.4 | 0.72 | 0.253 | 0.023 | 2 |

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
