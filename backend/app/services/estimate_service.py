from fastapi import HTTPException

from app.engines.wallpaper_math import roll_count
from app.modules.order_batch import InvalidSpare, apply_spare
from app.repositories import history, rolls, settings_repo, walls


def run_estimate(
    wall_id: int,
    roll_id: int,
    save: bool,
    note: str,
    spare_enabled: bool = False,
    spare_n: int | None = None,
):
    wall = walls.get_wall(wall_id)
    if not wall:
        raise HTTPException(404, "wall not found")
    roll = rolls.get_roll(roll_id)
    if not roll:
        raise HTTPException(404, "roll not found")
    if wall.get("data_quality") == "dirty" or roll.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty seed entity")

    calc = roll_count(
        wall["perimeter"], wall["height"], roll["width"], roll["length"], roll["pattern_cm"]
    )

    # Default N comes from settings but is copied onto this run, so later
    # changes to the default never move a historical run.
    if spare_enabled and spare_n is None:
        spare_n = settings_repo.get_spare_default_n()
    try:
        order = apply_spare(calc["rolls"], spare_enabled, spare_n if spare_n is not None else 0)
    except InvalidSpare as exc:
        # Validation failure for both dry and saved runs; nothing is persisted.
        raise HTTPException(422, str(exc))

    result = {**calc, **order, "wall_id": wall_id, "roll_id": roll_id}
    run_id = None
    if save:
        run_id = history.insert_run(wall_id, roll_id, result, note)
    return {"wall": wall, "roll": roll, "run_id": run_id, **result}
