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
_Updated 2026-10-29 01:15 UTC from PowderBench leaderboards._

### era5 — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-climatology | 0.0 | 0.97 | 0.382 | 0.030 | 107 |
| 2 | baseline-zeros | -1.1 | 1.01 | 0.506 | 0.033 | 107 |
| 3 | baseline-gfs | -24.7 | 0.80 | – | – | 107 |
| 4 | baseline-openmeteo | -33.0 | 0.88 | – | – | 107 |
| 5 | baseline-persistence | -202.1 | 1.50 | – | – | 107 |
| None | southern-league-mogger | 51.7 | 0.38 | 0.152 | 0.000 | 1 |

### observers — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| None | baseline-gem | 20.2 | 0.08 | – | – | 2 |
| None | baseline-icon | 16.0 | 0.08 | – | – | 2 |
| None | baseline-ukmo | 14.4 | 0.09 | – | – | 2 |
| None | baseline-consensus | 6.6 | 0.10 | – | – | 2 |
| None | baseline-zeros | 4.1 | 0.10 | 0.050 | 0.000 | 2 |
| None | baseline-ecmwf | 3.2 | 0.10 | – | – | 2 |

### resorts — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-openmeteo | 0.9 | 3.94 | – | – | 105 |
| 2 | baseline-zeros | 0.3 | 4.62 | 2.308 | 0.135 | 105 |
| 3 | baseline-climatology | 0.0 | 4.73 | 2.143 | 0.134 | 101 |
| 4 | baseline-gfs | -1.3 | 3.83 | – | – | 105 |
| 5 | baseline-persistence | -100.2 | 4.22 | – | – | 105 |
| None | baseline-icon | 8.9 | 0.24 | – | – | 4 |

### stations — not entered yet

| # | team | Powder Accuracy | MAE | pinball | Brier₆ | rounds |
|---|---|---|---|---|---|---|
| 1 | baseline-openmeteo | 15.0 | 1.78 | – | – | 9 |
| 2 | baseline-gfs | 12.6 | 1.53 | – | – | 11 |
| 3 | baseline-ukmo | 10.6 | 0.74 | – | – | 5 |
| 4 | baseline-icon | 3.2 | 0.80 | – | – | 5 |
| 5 | baseline-zeros | 0.3 | 2.04 | 1.021 | 0.068 | 11 |
| 6 | baseline-climatology | 0.0 | 1.98 | 0.698 | 0.062 | 11 |

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
