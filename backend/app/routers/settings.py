from fastapi import APIRouter
from app.repositories import settings_repo
from app.schemas.settings import SpareDefaultRequest

router = APIRouter()


@router.get("/settings")
def settings():
    return settings_repo.get_all()


@router.put("/settings/spare-default")
def set_spare_default(body: SpareDefaultRequest):
    # Only affects future runs that do not pin their own N; old runs stay as written.
    settings_repo.set_spare_default_n(body.spare_n)
    return {"spare_default_n": settings_repo.get_spare_default_n()}
