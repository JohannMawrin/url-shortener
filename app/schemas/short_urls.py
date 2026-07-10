from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class ShortURLPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    url: HttpUrl


class ShortURLPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    short_code: str
    created_at: datetime
    updated_at: datetime


class ShortURLStats(ShortURLPublic):
    access_count: int
