from datetime import datetime

from beanie import Document
from pydantic import Field

from app.core.time import utc_now


class Criterion(Document):
    business_id: str

    name: str
    weight: int
    minimum_required_score: int = 0
    active: bool = True

    created_at: datetime = Field(default_factory=utc_now)

    class Settings:
        name = "criteria"