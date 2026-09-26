from pydantic import BaseModel, Field


class EstimateRequest(BaseModel):
    wall_id: int
    roll_id: int
    save: bool = False
    note: str = ""
    spare_enabled: bool = False
    # Fixed spare count N. Must be non-negative; a negative value is rejected
    # here (and again in the service) before any run is written to history.
    spare_n: int | None = Field(default=None, ge=0)
