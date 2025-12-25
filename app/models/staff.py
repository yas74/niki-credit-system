from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field

from app.core.time import utc_now



class Staff(Document):
    full_name: str
    employee_code: Annotated[str, Indexed(unique=True)] 
    is_active: bool = True

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


    class Settings:
        name = "staff"