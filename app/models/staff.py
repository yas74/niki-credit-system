from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


UTC_NOW = lambda: datetime.now(timezone.utc)

class Staff(Document):
    full_name: str
    employee_code: Annotated[str, Indexed(unique=True)] 
    is_active: bool = True

    created_at: datetime = Field(default_factory=UTC_NOW)
    updated_at: datetime = Field(default_factory=UTC_NOW)


    class Settings:
        name = "staff"