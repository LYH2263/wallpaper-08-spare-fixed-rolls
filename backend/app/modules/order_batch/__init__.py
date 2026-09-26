"""Fixed spare rolls: order = base rolls + N when spare is enabled."""


class InvalidSpare(ValueError):
    """Raised when the fixed spare count N is negative."""


def apply_spare(base_rolls: int, spare_enabled: bool, spare_n: int) -> dict:
    """Return base rolls, the spare count N actually applied, and order rolls.

    When spare is disabled the order count equals the base count (pre-change
    behaviour) and N is pinned to 0. When enabled N must be non-negative;
    a negative N raises InvalidSpare so the caller can fail before persisting.
    """
    base = int(base_rolls)
    if not spare_enabled:
        return {"rolls": base, "spare_enabled": False, "spare_n": 0, "order_rolls": base}
    n = int(spare_n)
    if n < 0:
        raise InvalidSpare("spare_n must be >= 0")
    return {"rolls": base, "spare_enabled": True, "spare_n": n, "order_rolls": base + n}
