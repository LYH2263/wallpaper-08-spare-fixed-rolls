from fastapi import APIRouter, HTTPException
from app.repositories import history as repo

router = APIRouter()


@router.get("/runs")
def list_runs(limit: int = 50):
    return {"items": repo.list_runs(limit)}


@router.get("/runs/{run_id}")
def get_run(run_id: int):
    # Returned result_json is the snapshot pinned at write time: order rolls
    # and N never change even if the default N changes later.
    row = repo.get_run(run_id)
    if row is None:
        raise HTTPException(404, "run not found")
    return row
