from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field

from app.core.time import utc_now

class StaffCriterionScore(Document):
    business_id: str
    staff_id: str
    criterion_id: str

    score: int

    reviewed_by: str
    reviewed_at: datetime = Field(default_factory=utc_now)
    note: Optional[str] = None

    class Settings:
        name = "staff_criterion_scores"
