import pytest
from fastapi.testclient import TestClient

from app.engines.wallpaper_math import apply_spare
from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def _run_count(client):
    return len(client.get("/api/runs").json()["items"])


# --- engine ---

def test_apply_spare_disabled_keeps_base():
    r = apply_spare(11, False, 2)
    assert r == {"spare_enabled": False, "spare_n": 0, "order_rolls": 11}


def test_apply_spare_enabled_adds_fixed_n():
    r = apply_spare(11, True, 2)
    assert r == {"spare_enabled": True, "spare_n": 2, "order_rolls": 13}


def test_apply_spare_negative_rejected():
    with pytest.raises(ValueError):
        apply_spare(11, True, -1)


# --- dry-run branch ---

def test_dry_run_disabled_matches_legacy(client):
    r = client.get("/api/estimate", params={"wall_id": 1, "roll_id": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["rolls"] == 11
    assert body["spare_enabled"] is False
    assert body["spare_n"] == 0
    assert body["order_rolls"] == 11
    assert body["run_id"] is None


def test_dry_run_uses_settings_default(client):
    assert client.put("/api/settings/spare_default_n", json={"spare_default_n": 1}).status_code == 200
    before = _run_count(client)
    r = client.get("/api/estimate", params={"wall_id": 1, "roll_id": 1, "spare_enabled": "true"})
    assert r.status_code == 200
    body = r.json()
    assert body["rolls"] == 11
    assert body["spare_n"] == 1
    assert body["order_rolls"] == 12
    assert _run_count(client) == before  # dry run never writes history


def test_dry_run_explicit_n_overrides_default(client):
    r = client.get("/api/estimate", params={"wall_id": 1, "roll_id": 1, "spare_enabled": "true", "spare_n": 3})
    assert r.status_code == 200
    body = r.json()
    assert body["spare_n"] == 3
    assert body["order_rolls"] == 14


# --- persist branch ---

def test_save_pins_n_and_order_rolls(client):
    r = client.post("/api/estimate", json={"wall_id": 1, "roll_id": 1, "save": True,
                                           "spare_enabled": True, "spare_n": 2})
    assert r.status_code == 200
    run_id = r.json()["run_id"]
    assert run_id is not None

    got = client.get(f"/api/runs/{run_id}")
    assert got.status_code == 200
    result = got.json()["result"]
    assert result["rolls"] == 11
    assert result["spare_enabled"] is True
    assert result["spare_n"] == 2
    assert result["order_rolls"] == 13

    # changing the default afterwards must not move the saved run
    assert client.put("/api/settings/spare_default_n", json={"spare_default_n": 7}).status_code == 200
    again = client.get(f"/api/runs/{run_id}").json()["result"]
    assert again["spare_n"] == 2
    assert again["order_rolls"] == 13


def test_save_disabled_pins_zero_spare(client):
    r = client.post("/api/estimate", json={"wall_id": 1, "roll_id": 1, "save": True})
    assert r.status_code == 200
    result = client.get(f"/api/runs/{r.json()['run_id']}").json()["result"]
    assert result["spare_n"] == 0
    assert result["order_rolls"] == result["rolls"]


# --- validation ---

def test_negative_n_fails_and_history_not_grown(client):
    before = _run_count(client)
    r = client.post("/api/estimate", json={"wall_id": 1, "roll_id": 1, "save": True,
                                           "spare_enabled": True, "spare_n": -1})
    assert r.status_code == 422
    assert _run_count(client) == before


def test_negative_n_rejected_on_get(client):
    r = client.get("/api/estimate", params={"wall_id": 1, "roll_id": 1,
                                            "spare_enabled": "true", "spare_n": -2})
    assert r.status_code == 422


def test_negative_default_rejected(client):
    assert client.put("/api/settings/spare_default_n", json={"spare_default_n": -1}).status_code == 422


def test_settings_default_applies_to_new_runs(client):
    assert client.put("/api/settings/spare_default_n", json={"spare_default_n": 4}).status_code == 200
    body = client.get("/api/estimate", params={"wall_id": 1, "roll_id": 1, "spare_enabled": "true"}).json()
    assert body["spare_n"] == 4
    assert body["order_rolls"] == 15
