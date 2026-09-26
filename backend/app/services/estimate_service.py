from fastapi import HTTPException

from app.engines.wallpaper_math import apply_spare, roll_count
from app.repositories import history, rolls, settings_repo, walls


def _default_spare_n() -> int:
    raw = settings_repo.get_all().get("spare_default_n")
    try:
        return max(0, int(raw))
    except (TypeError, ValueError):
        return 0


def run_estimate(wall_id: int, roll_id: int, save: bool, note: str,
                 spare_enabled: bool = False, spare_n: int | None = None):
    wall = walls.get_wall(wall_id)
    if not wall:
        raise HTTPException(404, "wall not found")
    roll = rolls.get_roll(roll_id)
    if not roll:
        raise HTTPException(404, "roll not found")
    if wall.get("data_quality") == "dirty" or roll.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty seed entity")
    if spare_n is not None and spare_n < 0:
        raise HTTPException(422, "spare_n must be >= 0")

    calc = roll_count(
        wall["perimeter"], wall["height"], roll["width"], roll["length"], roll["pattern_cm"]
    )
    effective_n = spare_n if spare_n is not None else _default_spare_n()
    calc = {**calc, **apply_spare(calc["rolls"], spare_enabled, effective_n)}
    run_id = None
    if save:
        run_id = history.insert_run(wall_id, roll_id, {**calc, "wall_id": wall_id, "roll_id": roll_id}, note)
    return {"wall": wall, "roll": roll, "run_id": run_id, **calc}
