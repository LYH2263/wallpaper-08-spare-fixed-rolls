from typing import Optional

from pydantic import BaseModel, Field


class EstimateRequest(BaseModel):
    wall_id: int
    roll_id: int
    save: bool = False
    note: str = ""
    spare_enabled: bool = False
    spare_n: Optional[int] = Field(default=None, ge=0)
