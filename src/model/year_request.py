from pydantic import BaseModel, conint


class YearRequest(BaseModel):
    year: conint(ge=1970, le=2024) | None = None
