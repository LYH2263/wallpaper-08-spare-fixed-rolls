from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service

router = APIRouter()


@router.get("/estimate")
def estimate_get(
    wall_id: int = Query(...),
    roll_id: int = Query(...),
    save: bool = False,
    spare_enabled: bool = Query(False),
    spare_n: int | None = Query(default=None, ge=0),
):
    return estimate_service.run_estimate(
        wall_id, roll_id, save, "", spare_enabled, spare_n
    )


@router.post("/estimate")
def estimate_post(body: EstimateRequest):
    return estimate_service.run_estimate(
        body.wall_id, body.roll_id, body.save, body.note,
        body.spare_enabled, body.spare_n,
    )
