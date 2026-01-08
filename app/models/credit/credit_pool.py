from typing import Annotated
from datetime import datetime

from beanie import Document, Indexed
from pydantic import Field

from app.core.time import utc_now


class CreditPool(Document):
    business_id: Annotated[str, Indexed(unique=True)]
    balance: int = 0
    updated_at: datetime = Field(default_factory=utc_now)

    class Settings:
        name = "credit_pools"

