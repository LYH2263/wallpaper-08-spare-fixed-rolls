from pydantic import BaseModel, Field


class SpareDefaultUpdate(BaseModel):
    spare_default_n: int = Field(ge=0)
