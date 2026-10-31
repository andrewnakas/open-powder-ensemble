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
_Updated 2026-10-31 01:02 UTC from PowderBench leaderboards._

### era5 — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-climatology | 0.0 | 0.97 | 0.382 | 0.030 | 107 |
| 2 | baseline-zeros | -1.2 | 0.99 | 0.498 | 0.032 | 109 |
| 3 | baseline-gfs | -24.4 | 0.79 | – | – | 109 |
| 4 | baseline-openmeteo | -34.0 | 0.87 | – | – | 109 |
| 5 | baseline-persistence | -205.9 | 1.48 | – | – | 109 |
| None | southern-league-mogger | 51.7 | 0.38 | 0.152 | 0.000 | 1 |

### observers — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| None | baseline-wpc | 40.2 | 0.25 | 0.096 | 0.000 | 1 |
| None | house-blend | 34.5 | 0.26 | 0.099 | 0.000 | 1 |
| None | baseline-gem | 29.1 | 0.16 | – | – | 4 |
| None | baseline-ndfd | 27.2 | 0.25 | – | – | 1 |
| None | open-powder-ml | 25.7 | 0.29 | 0.126 | 0.000 | 1 |
| None | baseline-icon | 22.7 | 0.18 | – | – | 4 |

### resorts — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-zeros | 0.5 | 4.53 | 2.266 | 0.132 | 107 |
| 2 | baseline-climatology | 0.0 | 4.64 | 2.104 | 0.131 | 103 |
| 3 | baseline-openmeteo | -2.0 | 3.88 | – | – | 107 |
| 4 | baseline-icon | -7.3 | 0.25 | – | – | 6 |
| 5 | baseline-gfs | -8.0 | 3.77 | – | – | 107 |
| 6 | baseline-gem | -13.7 | 0.26 | – | – | 6 |

### stations — **#None** of 16 (Powder Accuracy 47.8, 1 rounds, not yet ranked)

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-consensus | 20.2 | 0.69 | – | – | 6 |
| 2 | baseline-ukmo | 18.0 | 0.74 | – | – | 7 |
| 3 | baseline-openmeteo | 11.5 | 1.67 | – | – | 11 |
| 4 | baseline-gfs | 9.9 | 1.48 | – | – | 13 |
| 5 | baseline-icon | 7.7 | 0.84 | – | – | 7 |
| 6 | baseline-climatology | 0.0 | 1.86 | 0.662 | 0.054 | 13 |
| None | **open-powder-ensemble** | 47.8 | 0.68 | 0.224 | 0.011 | 1 |

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
