from fastapi import APIRouter
from app.repositories import settings_repo
from app.schemas.settings import SpareDefaultUpdate

router = APIRouter()


@router.get("/settings")
def settings():
    return settings_repo.get_all()


@router.put("/settings/spare_default_n")
def set_spare_default(body: SpareDefaultUpdate):
    settings_repo.set_value("spare_default_n", str(body.spare_default_n))
    return {"spare_default_n": body.spare_default_n}
