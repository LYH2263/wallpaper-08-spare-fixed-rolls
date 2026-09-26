import os
import pathlib

import pytest

_TMP = pathlib.Path("/tmp/wp_test_data")
_TMP.mkdir(parents=True, exist_ok=True)
os.environ["DATA_DIR"] = str(_TMP)


@pytest.fixture
def client():
    db = _TMP / "app.db"
    if db.exists():
        db.unlink()
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as c:
        yield c


def _run_count():
    from app.repositories import history
    return len(history.list_runs(10000))


def test_dry_run_without_spare_matches_base(client):
    r = client.get("/api/estimate?wall_id=1&roll_id=1").json()
    assert r["rolls"] == 11
    assert r["spare_enabled"] is False
    assert r["order_rolls"] == 11


def test_dry_run_with_spare(client):
    r = client.get("/api/estimate?wall_id=1&roll_id=1&spare_enabled=true&spare_n=2").json()
    assert r["rolls"] == 11
    assert r["spare_n"] == 2
    assert r["order_rolls"] == 13
    assert _run_count() == 0  # dry run never persists


def test_negative_n_get_fails_without_history(client):
    before = _run_count()
    resp = client.get("/api/estimate?wall_id=1&roll_id=1&spare_enabled=true&spare_n=-1")
    assert resp.status_code == 422
    assert _run_count() == before


def test_negative_n_post_save_fails_without_history(client):
    before = _run_count()
    resp = client.post("/api/estimate", json={
        "wall_id": 1, "roll_id": 1, "save": True,
        "spare_enabled": True, "spare_n": -3,
    })
    assert resp.status_code == 422
    assert _run_count() == before


def test_saved_run_pins_n_and_order_rolls(client):
    resp = client.post("/api/estimate", json={
        "wall_id": 1, "roll_id": 1, "save": True,
        "spare_enabled": True, "spare_n": 2,
    })
    assert resp.status_code == 200
    run_id = resp.json()["run_id"]

    got = client.get(f"/api/runs/{run_id}").json()
    assert got["result"]["rolls"] == 11
    assert got["result"]["spare_n"] == 2
    assert got["result"]["order_rolls"] == 13


def test_changing_default_n_does_not_move_old_run(client):
    run_id = client.post("/api/estimate", json={
        "wall_id": 1, "roll_id": 1, "save": True,
        "spare_enabled": True, "spare_n": 2,
    }).json()["run_id"]

    upd = client.put("/api/settings/spare-default", json={"spare_n": 9})
    assert upd.status_code == 200
    assert upd.json()["spare_default_n"] == 9

    # Old run still reports the pinned values from write time.
    got = client.get(f"/api/runs/{run_id}").json()
    assert got["result"]["spare_n"] == 2
    assert got["result"]["order_rolls"] == 13

    # A new enabled run without an explicit N picks up the new default.
    fresh = client.get("/api/estimate?wall_id=1&roll_id=1&spare_enabled=true").json()
    assert fresh["spare_n"] == 9
    assert fresh["order_rolls"] == 20


def test_negative_default_n_rejected(client):
    assert client.put("/api/settings/spare-default", json={"spare_n": -1}).status_code == 422
