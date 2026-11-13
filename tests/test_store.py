from pathlib import Path

from ope import store


def test_ens_units_go_to_their_years_release():
    assert store.ens_tag("ens__gfsf__stations-net__2026-10.parquet") == "ens-store-2026"
    assert store.ens_tag("ens__gefs__era5__2021-01.parquet") == "ens-store-2021"


def test_push_ens_routes_by_year_and_replaces_in_place(monkeypatch):
    pushed = {}
    monkeypatch.setattr(store, "remote_assets", lambda tag: {"ens__gefs__alps__2024-12.parquet"})
    monkeypatch.setattr(store, "push", lambda tag, files: pushed.setdefault(tag, []).extend(f.name for f in files))
    store.push_ens([Path("ens__gefs__alps__2024-12.parquet"), Path("ens__gefs__alps__2026-10.parquet"),
                    Path("ens__hrrrf__stations__2026-10.parquet")])
    assert pushed == {"ens-store": ["ens__gefs__alps__2024-12.parquet"],
                      "ens-store-2026": ["ens__gefs__alps__2026-10.parquet", "ens__hrrrf__stations__2026-10.parquet"]}


def test_ens_tags_lists_the_whole_family(monkeypatch):
    class R:
        returncode, stdout, stderr = 0, "models\nens-store-2026\nsnowpack\nens-store\nens-store-2025\n", ""

    monkeypatch.setenv("OPE_REPO", "x/y")
    monkeypatch.setattr(store, "_gh", lambda *a: R)
    assert store.ens_tags() == ["ens-store", "ens-store-2025", "ens-store-2026"]
