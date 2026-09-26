import pytest

from app.modules.order_batch import InvalidSpare, apply_spare


def test_disabled_order_equals_base():
    r = apply_spare(11, False, 5)
    assert r["rolls"] == 11
    assert r["spare_enabled"] is False
    assert r["spare_n"] == 0
    assert r["order_rolls"] == 11


def test_enabled_adds_fixed_n():
    r = apply_spare(11, True, 2)
    assert r["rolls"] == 11
    assert r["spare_enabled"] is True
    assert r["spare_n"] == 2
    assert r["order_rolls"] == 13


def test_zero_n_keeps_base():
    assert apply_spare(7, True, 0)["order_rolls"] == 7


def test_negative_n_fails():
    with pytest.raises(InvalidSpare):
        apply_spare(11, True, -1)
