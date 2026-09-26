from pydantic import BaseModel, Field


class SpareDefaultRequest(BaseModel):
    # Default fixed spare count N maintained on the settings page.
    spare_n: int = Field(ge=0)
